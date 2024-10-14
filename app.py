from flask import Flask, render_template, jsonify
import speech_recognition as sr
import threading

app = Flask(__name__)

recognizer = sr.Recognizer()
transcription = ""  # This will hold the real-time transcription


def transcribe_audio():
    global transcription
    while True:
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise and listen
                recognizer.adjust_for_ambient_noise(source)
                print("Listening...")
                audio = recognizer.listen(source)
                
                # Recognize speech using Google Web Speech API
                print("Recognizing...")
                transcription = recognizer.recognize_google(audio)
                print(f"Transcription: {transcription}")
        except sr.UnknownValueError:
            transcription = "Sorry, I could not understand the audio."
        except sr.RequestError:
            transcription = "Sorry, there was a request error."


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/transcription')
def get_transcription():
    return jsonify({"text": transcription})


if __name__ == '__main__':
    # Start the audio transcription in a separate thread
    transcription_thread = threading.Thread(target=transcribe_audio)
    transcription_thread.start()
    
    # Run the Flask app
    app.run(debug=True, use_reloader=False)
