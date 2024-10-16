from flask import Flask, render_template, request, jsonify
import assemblyai as aai
import os
import tempfile

# Initialize Flask app
app = Flask(__name__)

# Set your AssemblyAI API Key
AIA_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
print(f"API Key retrieved: {AIA_API_KEY}")  # Debugging: print the API key

if not AIA_API_KEY:
    raise ValueError("Missing AssemblyAI API Key. Set it in your environment variables.")

aai.settings.api_key = "d6c1bc9c65e442cf974d3aeda69fa830"
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
        transcript = transcriber.transcribe(audio_path)
        if not transcript.success:
            return jsonify({"error": "Transcription failed"}), 500
        return jsonify({"text": transcript.text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
