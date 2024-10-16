let mediaRecorder;
let audioChunks = [];
let audioContext;
let analyser;
let microphone;
let silenceTimeout;

navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => console.log("Microphone active"))
    .catch(err => console.error("Microphone error", err));

// Voice Activity Detection and Audio Capture
async function startListening() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    audioContext = new AudioContext();
    analyser = audioContext.createAnalyser();
    microphone = audioContext.createMediaStreamSource(stream);
    microphone.connect(analyser);

    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = function(event) {
        audioChunks.push(event.data);
        if (mediaRecorder.state === "inactive") {
            sendAudioToServer(audioChunks);
        }
    };

    detectVoice();
}

function detectVoice() {
    const bufferLength = analyser.fftSize;
    const dataArray = new Uint8Array(bufferLength);

    function analyzeAudio() {
        analyser.getByteTimeDomainData(dataArray);
        const maxVolume = Math.max(...dataArray);

        // Adjust the sensitivity threshold here
        if (maxVolume > 100) {  // Try lowering to 100 or less
            console.log("Voice detected. Recording...");
            if (mediaRecorder.state === "inactive") {
                audioChunks = [];
                mediaRecorder.start();
            }
            // Reset silence timeout
            clearTimeout(silenceTimeout);
            silenceTimeout = setTimeout(stopRecording, 2000); // Stop recording after 2 seconds of silence
        }
        requestAnimationFrame(analyzeAudio);
    }

    analyzeAudio();
}

function stopRecording() {
    console.log("Stopping recording due to silence.");
    if (mediaRecorder.state === "recording") {
        mediaRecorder.stop();
    }
}

function sendAudioToServer(chunks) {
    const blob = new Blob(chunks, { type: 'audio/wav; codecs=opus' });
    const formData = new FormData();
    formData.append('file', blob, 'audio.wav');

    fetch('/transcribe', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('transcription').textContent = data.text;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Start listening for voice input on page load
window.onload = startListening;
