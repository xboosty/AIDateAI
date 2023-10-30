from flask import Flask, request, jsonify, redirect
from flasgger import Swagger, swag_from
from transcription import transcribe_audio
import speech_recognition as sr
import os
import whisper

app = Flask(__name__)
swagger = Swagger(app)
app.config['SWAGGER'] = {'doc_expansion': 'list'}


@app.route('/transcribe-audio-google', methods=['POST'])
#@swag_from('swagger/google_transcription.yml')
def transcribe_audio_google():
    """
    Transcribe audio using Google Speech Recognition API.
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: audio
        in: formData
        type: file
        required: true
        description: Audio file to transcribe.
    responses:
      200:
        description: Text transcribed from the audio file.
        schema:
          type: object
          properties:
            text_result:
              type: string
      400:
        description: Bad request.
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Internal server error.
        schema:
          type: object
          properties:
            error:
              type: string
    """
    if 'audio' not in request.files:
        return jsonify({'error': 'Audio file not provided'}), 400

    audio = request.files['audio']
    _, ext = os.path.splitext(audio.filename)
    if ext not in ('.wav'):
        return jsonify({'error': 'Invalid file format'}), 400

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

@app.route('/transcribe-audio-openai-small', methods=['POST'])
#@swag_from('swagger/whisper_transcription.yml')
def transcribe_audio_openai_small():
    """
    Transcribe audio using OpenAI Whisper (small model).
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: audio
        in: formData
        type: file
        required: true
        description: Audio file to transcribe.
    responses:
      200:
        description: Text transcribed from the audio file.
        schema:
          type: object
          properties:
            text_result:
              type: string
      400:
        description: Bad request.
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Internal server error.
        schema:
          type: object
          properties:
            error:
              type: string
    """
    if 'audio' not in request.files:
        return jsonify({'error': 'Audio file not provided'}), 400

    audio = request.files['audio']
    return transcribe_audio(model_whisper_small, audio)

@app.route('/transcribe-audio-openai-medium', methods=['POST'])
#@swag_from('swagger/whisper_transcription.yml')
def transcribe_audio_openai_medium():
    """
    Transcribe audio using OpenAI Whisper (medium model).
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: audio
        in: formData
        type: file
        required: true
        description: Audio file to transcribe.
    responses:
      200:
        description: Text transcribed from the audio file.
        schema:
          type: object
          properties:
            text_result:
              type: string
      400:
        description: Bad request.
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Internal server error.
        schema:
          type: object
          properties:
            error:
              type: string
    """
    if 'audio' not in request.files:
        return jsonify({'error': 'Audio file not provided'}), 400

    audio = request.files['audio']
    return transcribe_audio(model_whisper_medium, audio)

if __name__ == '__main__':
    model_whisper_small = whisper.load_model("small")
    model_whisper_medium = whisper.load_model("medium")
    app.run()