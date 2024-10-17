from flask import Flask, render_template, request, jsonify
import assemblyai as aai
import os
import tempfile
import time

# Initialize Flask app
app = Flask(__name__)

# Set your AssemblyAI API Key
AIA_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
print(f"API Key retrieved: {AIA_API_KEY}")  # Debugging: print the API key

if not AIA_API_KEY:
    raise ValueError("Missing AssemblyAI API Key. Set it in your environment variables.")

aai.settings.api_key = AIA_API_KEY
transcriber = aai.Transcriber()

# Root route to serve the index.html page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle audio file transcription
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    # Save the uploaded file temporarily
    audio_file = request.files['file']
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
        audio_file.save(temp_audio_file.name)
        audio_path = temp_audio_file.name

    # Use AssemblyAI to transcribe the file
    try:
        transcript_response = transcriber.transcribe(audio_path)
        while not transcript_response.success:
            time.sleep(5)  # Polling the result with a 5-second delay
            transcript_response = transcriber.get_transcription(transcript_response.id)
        return jsonify({"text": transcript_response.text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
