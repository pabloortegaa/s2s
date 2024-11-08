from flask import Flask, render_template, request, jsonify
import os
import speech_recognition as sr
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Route to handle audio file upload and transcription
@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    recognizer = sr.Recognizer()

    try:
        # Save the file temporarily
        filename = secure_filename(audio_file.filename)
        audio_path = os.path.join('/tmp', filename)
        audio_file.save(audio_path)

        # Transcribe audio
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        os.remove(audio_path)  # Clean up the temporary file
        return jsonify({"transcription": text})

    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand the audio"}), 400
    except sr.RequestError as e:
        return jsonify({"error": f"API request error: {str(e)}"}), 500

if __name__ == '__main__':
    port = os.environ.get('FLASK_PORT') or 8080
    port = int(port)
    app.run(port=port, host='0.0.0.0')
