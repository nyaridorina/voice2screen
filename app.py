from flask import Flask, request, jsonify
import assemblyai as aai
import os

# Initialize Flask app
app = Flask(__name__)

# Set your AssemblyAI API Key
AIA_API_KEY = os.getenv("ASSEMBLYAI_API_KEY", "d6c1bc9c65e442cf974d3aeda69fa830")
aai.settings.api_key = AIA_API_KEY
transcriber = aai.Transcriber()

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    audio_file = request.files['file']
    audio_path = os.path.join("/tmp", audio_file.filename)
    audio_file.save(audio_path)

    # Use AssemblyAI to transcribe the file
    try:
        transcript = transcriber.transcribe(audio_path)
        return jsonify({"text": transcript.text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
