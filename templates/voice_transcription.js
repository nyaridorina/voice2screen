let mediaRecorder;
let audioChunks = [];
let audioContext;
let analyser;
let microphone;
let silenceTimeout;

// Check microphone access and handle error
navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        console.log("Microphone active");
        startListening(stream);  // Call main function if mic is active
    })
    .catch(err => {
        console.error("Microphone error:", err);
        document.getElementById('transcription').textContent = "Microphone access denied.";
    });

// Start listening to the microphone
function startListening(stream) {
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

// Voice detection and audio analysis
function detectVoice() {
    const bufferLength = analyser.fftSize;
    const dataArray = new Uint8Array(bufferLength);

    function analyzeAudio() {
        analyser.getByteTimeDomainData(dataArray);
        const maxVolume = Math.max(...dataArray);

        console.log("Max volume:", maxVolume); // Debugging to track audio levels

        if (maxVolume > 100) {  // Adjust the sensitivity threshold here
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

// Stop recording after silence
function stopRecording() {
    console.log("Stopping recording due to silence.");
    if (mediaRecorder.state === "recording") {
        mediaRecorder.stop();
    }
}

// Send recorded audio to the server
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
