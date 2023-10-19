import speech_recognition as sr

class Transcriptor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
    
    def transcribe_audio_to_text(self,filename):
        recognizer = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio = recognizer.record(source)
        try:
            return recognizer.recognize_google(audio)
        except:
            print('Skipping unknown error')