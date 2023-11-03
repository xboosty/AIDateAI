import os
import librosa
import numpy as np
#import whisper
import time
import random

import speech_recognition as sr
from fastapi import UploadFile
from fastapi.responses import JSONResponse

def transcribe_speech_reconigtion(audio: UploadFile):
    if audio is None:
        return JSONResponse(content={'error': 'Audio file not provided'}, status_code=400)

    _, ext = os.path.splitext(audio.filename)
    if ext not in ('.wav'):
        return JSONResponse(content={'error': 'Invalid file format'}, status_code=400)

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio.file) as source:
            audio_data = recognizer.record(source)
            text_result = recognizer.recognize_google(audio_data)  # Utiliza Google Web Speech API para la transcripción

        return {'text_result': text_result}
    except sr.UnknownValueError:
        return {'error': 'Audio could not be transcribed'}
    except Exception as e:
        print({'error': str(e)})
        return {'error': str(e)}

#def transcribe_audio_to_text(filename, model_whisper):
#    try:
#        if os.path.exists(filename):
#            audio, sr = librosa.load(filename, mono=True)
#            audio_norm = librosa.util.normalize(audio)
#            aud_array = audio_norm.astype(np.float32)
#
#            transcript = model_whisper.transcribe(
#                audio=aud_array,
#                fp16=False
#            )
#            return transcript['text']
#        else:
#            raise Exception("The file does not exist in the specified location.")
#
#    except Exception as e:
#        return "An error occurred during transcription: {}".format(e)
#
#def transcribe_audio(model, audio):    
#    try:
#        temp_audio_path = os.path.join(os.getcwd(), audio.filename)
#        text_result = transcribe_audio_to_text(temp_audio_path, model)
#        return {'text_result': text_result}, 200
#    except Exception as e:
#        return {'error': str(e)}, 500
#    finally:
#        print("Deleting temp audio file: {}".format(temp_audio_path))
#        os.remove(temp_audio_path)
#        
#def transcribe_audio_no_delete(model,full_path):    
#    try:        
#        text_result = transcribe_audio_to_text(full_path, model)
#        return text_result
#    except Exception as e:
#        return {'error': str(e)}, 500