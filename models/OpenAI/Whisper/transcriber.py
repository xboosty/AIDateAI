import openai
import whisper

#Convertir audio en texto
class Transcriber:
    def __init__(self):
        pass
        
    #Siempre guarda y lee del archivo audio.mp3
    #Utiliza whisper en la nube :) puedes cambiarlo por una impl local
    def transcribe(self, audio):
        audio.save("audio.mp3")
        audio_file= open("audio.mp3", "rb")
        transcript = whisper.transcribe(audio_file)
        return transcript.text