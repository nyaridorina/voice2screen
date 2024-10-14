from flask import Flask, render_template, jsonify
import speech_recognition as sr

app = Flask(__name__)

recognizer = sr.Recognizer()

def recognize_speech():
    with sr.AudioFile(source) as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing speech...")
        text = recognizer.recognize_google(audio)  # Using Google's API for recognition
        return text
    except sr.UnknownValueError:
        return "Sorry, I could not understand the audio."
    except sr.RequestError:
        return "Sorry, there was a request error."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe')
def transcribe():
    text = recognize_speech()
    return jsonify({"text": text})

if __name__ == '__main__':
    app.run(debug=True)
