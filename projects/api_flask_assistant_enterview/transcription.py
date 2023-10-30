import os
import librosa
import numpy as np
import whisper
import time
import random

def transcribe_audio_to_text(filename, model_whisper):
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
        return {'error': 'Invalid file format'}, 400

    current_time_ms = int(round(time.time() * 1000))
    random_number = random.randint(100000, 999999)
    audio_name = 'audio_'+str(current_time_ms)+'_'+str(random_number) + ext
    temp_audio_path = os.path.join(os.getcwd(), audio_name)
    try:
        audio.save(temp_audio_path)
        return temp_audio_path
    except Exception as e:
        return {'error': str(e)}, 500

def transcribe_audio(model, audio):
    try:
        temp_audio_path = save_audio(audio)
        text_result = transcribe_audio_to_text(temp_audio_path, model)
        return {'text_result': text_result}, 200
    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        os.remove(temp_audio_path)