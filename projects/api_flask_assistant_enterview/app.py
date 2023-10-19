from flask import Flask, request, jsonify
import speech_recognition as sr
import whisper
import os
import tempfile
import librosa
import io
import numpy as np
from scipy.io.wavfile import read as wav_read
from scipy.io.wavfile import write
from base64 import b64decode
import time
import random

app = Flask(__name__)


@app.route('/transcribe-audio-google', methods=['GET'])
def transcribe_audio_google():
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
    
    
    
@app.route('/transcribe-audio-openai-small', methods=['GET'])
def transcribe_audio_openai_small():
    if 'audio' not in request.files:
        return jsonify({'error': 'Audio file not provided'}), 400

    audio = request.files['audio']
    try:
        temp_audio_path = save_audio(audio)
        text_result = transcribe_audio_to_text(temp_audio_path,model_whisper_small)
        return jsonify({'text_result': text_result})
    except sr.UnknownValueError:
        return jsonify({'error': 'Audio could not be transcribed',
                        'temp_audio_path':temp_audio_path}), 400
    except Exception as e:
        return jsonify({'error': str(e),
                        'temp_audio_path':temp_audio_path}), 500
    finally:
        os.remove(temp_audio_path) 
        
@app.route('/transcribe-audio-openai-medium', methods=['GET'])
def transcribe_audio_openai_medium():
    if 'audio' not in request.files:
        return jsonify({'error': 'Audio file not provided'}), 400

    audio = request.files['audio']
    try:
        temp_audio_path = save_audio(audio)
        text_result = transcribe_audio_to_text(temp_audio_path,model_whisper_medium)
        return jsonify({'text_result': text_result})
    except sr.UnknownValueError:
        return jsonify({'error': 'Audio could not be transcribed',
                        'temp_audio_path':temp_audio_path}), 400
    except Exception as e:
        return jsonify({'error': str(e),
                        'temp_audio_path':temp_audio_path}), 500
    finally:
        os.remove(temp_audio_path) 


#FUNCIONES AUXILIARES
def transcribe_audio_to_text(filename,model_whisper):
    try:
        if os.path.exists(filename):
            audio, sr = librosa.load(filename, mono=True)
            audio_norm = librosa.util.normalize(audio)
            aud_array = audio_norm.astype(np.float32)
            
            transcript = model_whisper.transcribe(
                audio=aud_array,
                fp16=False
            )                    
            return transcript['text']
        else:
            return "The file does not exist in the specified location."  
        
    except Exception as e:
        return "An error occurred during transcription: {}".format(e) 

        
def save_audio(audio):
    _, ext = os.path.splitext(audio.filename)
    if ext not in ('.wav', '.mp3'):
        return jsonify({'error': 'Invalid file format'}), 400
    
    current_time_ms = int(round(time.time() * 1000))
    random_number = random.randint(100000, 999999)
    audio_name = 'audio_'+str(current_time_ms)+'_'+str(random_number) + ext
    temp_audio_path = os.path.join(app.root_path, audio_name)
    try:        
        audio.save(temp_audio_path)
        return temp_audio_path
    except Exception as e:
        return jsonify({'error': str(e)}), 500  
     
    
if __name__ == '__main__':
    model_whisper_small = whisper.load_model("small")
    model_whisper_medium = whisper.load_model("medium")
    app.run()
