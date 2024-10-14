from flask import Flask, render_template, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

recognizer = sr.Recognizer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    with sr.AudioFile(file) as source:
        audio = recognizer.record(source)
    
    try:
        # Use Google Web Speech API for transcription
        text = recognizer.recognize_google(audio)
        return jsonify({"text": text})
    except sr.UnknownValueError:
        return jsonify({"text": "Sorry, I could not understand the audio."})
    except sr.RequestError as e:
        return jsonify({"text": f"Request error: {e}"})


if __name__ == '__main__':
    app.run(debug=True)
