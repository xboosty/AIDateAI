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
            raise Exception("The file does not exist in the specified location.")

    except Exception as e:
        return "An error occurred during transcription: {}".format(e)

def transcribe_audio(model, audio):    
    try:
        temp_audio_path = os.path.join(os.getcwd(), audio.filename)
        text_result = transcribe_audio_to_text(temp_audio_path, model)
        return {'text_result': text_result}, 200
    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        print("Deleting temp audio file: {}".format(temp_audio_path))
        os.remove(temp_audio_path)
        
def transcribe_audio_no_delete(model,full_path):    
    try:        
        text_result = transcribe_audio_to_text(full_path, model)
        return text_result
    except Exception as e:
        return {'error': str(e)}, 500