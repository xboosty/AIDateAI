from flask import Flask, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

@app.route('/transcribe_audio', methods=['POST'])
def transcribe_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'Audio file not provided'}), 400

    audio = request.files['audio']
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio) as source:
            audio_data = recognizer.record(source)
            text_result = recognizer.recognize_google(audio_data)  # Utiliza Google Web Speech API para la transcripción

        return jsonify({'text_result': text_result})
    except sr.UnknownValueError:
        return jsonify({'error': 'Audio could not be transcribed'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
