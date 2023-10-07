import openai
import pyttsx3
import speech_recognition as sr
import time

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

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print('Skipping unknown error')

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    i=0
    # Read presentation using text-to-speech
    speak_text (presentation)
    while i<len(questions):
        # Wait for user to say the word Start or the word Ready to begin the questions
        #print("Say 'Start' or 'Ready' to begin the questions...")
        #speak_text ("Say 'Start' or 'Ready' to begin the questions")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            #audio = recognizer.listen(source)
            try:
                #transcription = recognizer.recognize_google (audio)
                if True: #transcription.lower() in ["start","ready"] :
                    # Record audio
                    filename = "answer_"+str(i)+".wav"
                    filename_text = "answer_"+str(i)+".txt"
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

