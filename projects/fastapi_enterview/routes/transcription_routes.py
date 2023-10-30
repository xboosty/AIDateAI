from ai.transcription import transcribe_audio
import speech_recognition as sr
import os
import whisper
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
import speech_recognition as sr
import shutil

model_whisper_small = whisper.load_model("small")
model_whisper_medium = whisper.load_model("medium")
router_transcription = APIRouter()

@router_transcription.post('/ai/transcribe-audio-google')
def transcribe_audio_google(audio: UploadFile):
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

        return JSONResponse(content={'text_result': text_result}, status_code=200)
    except sr.UnknownValueError:
        return JSONResponse(content={'error': 'Audio could not be transcribed'}, status_code=400)
    except Exception as e:
        return JSONResponse(content={'error': str(e)}, status_code=500)
    

@router_transcription.post('/ai/transcribe-audio-openai-small')
def transcribe_audio_openai_small(audio: UploadFile):    
    return transcribe_audio(model_whisper_small, upload_file(audio))

@router_transcription.post('/ai/transcribe-audio-openai-medium')
def transcribe_audio_openai_medium(audio: UploadFile):
    return transcribe_audio(model_whisper_medium, upload_file(audio))

def upload_file(file: UploadFile = File(...)):
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file