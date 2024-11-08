from flask import Flask, jsonify
import os
import speech_recognition as sr

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello Worldddd!"

# Health check route
@app.route('/health')
def health():
    return "OK"

# Transcribe route
@app.route('/transcribe', methods=['GET'])
def transcribe_audio():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            audio = recognizer.listen(source)
            print("Processing...")

        # Recognize speech using Google Web Speech API
        text = recognizer.recognize_google(audio)
        return jsonify({"transcription": text})
    
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand the audio"}), 400
    except sr.RequestError as e:
        return jsonify({"error": f"API request error: {str(e)}"}), 500

if __name__ == '__main__':
    port = os.environ.get('FLASK_PORT') or 8080
    port = int(port)
    app.run(port=port, host='0.0.0.0')
