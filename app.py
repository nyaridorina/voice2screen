from flask import Flask, render_template, request, jsonify
import requests
import os
import tempfile
import time
import logging

# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set your AssemblyAI API Key
AIA_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
logging.info(f"API Key retrieved: {AIA_API_KEY}")  # Debugging: log the API key

if not AIA_API_KEY:
    raise ValueError("Missing AssemblyAI API Key. Set it in your environment variables.")

HEADERS = {'authorization': AIA_API_KEY}

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
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
        audio_file.save(temp_audio_file.name)
        audio_path = temp_audio_file.name

    # Upload the audio file to AssemblyAI
    try:
        with open(audio_path, 'rb') as f:
            response = requests.post('https://api.assemblyai.com/v2/upload', headers=HEADERS, data=f)
            response.raise_for_status()
            upload_url = response.json()['upload_url']
            logging.info(f"File uploaded successfully: {upload_url}")
    except Exception as e:
        logging.error(f"Failed to upload audio file: {str(e)}")
        return jsonify({"error": f"Failed to upload audio file: {str(e)}"}), 500

    # Request transcription
    try:
        transcript_request = {
            "audio_url": upload_url
        }
        transcript_response = requests.post('https://api.assemblyai.com/v2/transcript', json=transcript_request, headers=HEADERS)
        transcript_response.raise_for_status()
        transcript_id = transcript_response.json()['id']
        logging.info(f"Transcription requested successfully: {transcript_id}")
    except Exception as e:
        logging.error(f"Failed to request transcription: {str(e)}")
        return jsonify({"error": f"Failed to request transcription: {str(e)}"}), 500

    # Poll for transcription result with a retry limit
    try:
        transcript_status_url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
        max_retries = 12  # Retry for 1 minute (5 seconds * 12 retries)
        retries = 0
        while retries < max_retries:
            transcript_result = requests.get(transcript_status_url, headers=HEADERS)
            transcript_result.raise_for_status()
            result = transcript_result.json()
            if result['status'] == 'completed':
                logging.info("Transcription completed successfully.")
                return jsonify({"text": result['text']}), 200
            elif result['status'] == 'failed':
                logging.error("Transcription failed.")
                return jsonify({"error": "Transcription failed"}), 500
            retries += 1
            time.sleep(5)  # Polling interval
        logging.error("Transcription polling timed out.")
        return jsonify({"error": "Transcription polling timed out"}), 500
    except Exception as e:
        logging.error(f"Error during transcription polling: {str(e)}")
        return jsonify({"error": f"Error during transcription polling: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
