import openai
import whisper

class Transcriber:
    def __init__(self):
        pass
        
    #transcribe audio to text
    def transcribe(self, audio):
        audio.save("audio.mp3")
        audio_file= open("audio.mp3", "rb")
        transcript = whisper.transcribe(audio_file)
        return transcript.text
    
    #transcribe audio to english text 
    def translate(self, audio):
        audio.save("audio.mp3")
        audio_file= open("audio.mp3", "rb")
        translate = whisper.translate(audio_file)
        return translate.text