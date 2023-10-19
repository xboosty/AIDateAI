import openai
import pyttsx3
import whisper
import speech_recognition as sr
import time
import os
import numpy as np

#START TEXT TO SPEECH AS engine
engine = pyttsx3.init()
presentation = "Hello, I am the virtual assistant designed to conduct our interview with you."
questions = [
    "How many children do you have?",
    "You like children?",
    "What is your favorite color?",
    "What do you think about the war in Ukraine?",
    "How do you define yourself?",
    "What is your sexual orientation? If you think it is better not to answer, say that you will not answer this question.",
    "What types of people are you interested in meeting?"
]

model_whisper = whisper.load_model("small")#cambiar por large para mejores resultados

def transcribe_audio_to_text(filename):
    try:               
        # load audio and pad/trim it to fit 30 seconds
        # transcript = model_whisper.transcribe(audio=audio_bytes,model='whisper')
        if os.path.exists(filename):
            # Realizar acciones en el archivo aquí
            with open(filename, 'rb') as audio_file:
                audio_bytes = audio_file.read() 
            aud_array = np.frombuffer(audio_bytes, np.int8).flatten().astype(np.float32) / 32768.0
            transcript = model_whisper.transcribe(audio=aud_array,fp16=False)        
            return transcript['text']
        else:
            print("El archivo no existe en la ubicación especificada.")  
        
    except Exception as e:
        print("An error occurred during transcription: {}".format(e))      

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    i=0
    # Read presentation using text-to-speech
    speak_text (presentation)
    while i<len(questions):
        try:
            #transcription = recognizer.recognize_google (audio)
            if True: #transcription.lower() in ["start","ready"] :
                # Record audio
                filename = "user_answer_"+str(i)+".wav"
                filename_text = "user_answer_"+str(i)+".txt"
                print(questions[i])
                # Read question using text-to-speech
                speak_text (questions[i])
                i+=1
                with sr.Microphone() as source:
                    recognizer = sr.Recognizer()
                    source.pause_threshold = 1
                    audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                    with open(filename, "wb") as f:
                        f.write(audio.get_wav_data())
                # Transcribe audio to text
                text = transcribe_audio_to_text(filename)
                if text:
                    print(f"You said: {text}")
                    with open(filename_text,"w") as f:
                        f.write(text)                        
        except Exception as e:
            print("An error occurred: {}".format(e))    

if __name__ == "__main__":
    main()

