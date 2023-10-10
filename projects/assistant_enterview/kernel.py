import speech_recognition as sr
from conversations.conversations import Conversation
from transcription.transcription import Transcriptor
from files.files import Files

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

conversation = Conversation(presentation,questions)

transcriptor = Transcriptor()

files = Files()

path_audio = files.getConcatPathToRoot("audio_users_temp")

def main():
    i=0
    # Read presentation using text-to-speech
    conversation.speakPresentation()
    questions = conversation.getQuestions()
    while i<len(questions):
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            try:
                # Record audio
                filename = "answer_"+str(i)+".wav"
                filename_text = "answer_"+str(i)+".txt"
                print(questions[i])
                # Read question using text-to-speech
                conversation.speakQuestion(i)
                i+=1
                with sr.Microphone() as source:
                    recognizer = sr.Recognizer()
                    source.pause_threshold = 1
                    audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                    with open(files.joinPath(path_audio, filename), "wb") as f:
                        f.write(audio.get_wav_data())
                # Transcribe audio to text                    
                text = transcriptor.transcribe_audio_to_text(files.joinPath(path_audio, filename))
                if text:
                    print(f"You said: {text}")
                    with open(files.joinPath(path_audio, filename_text),"w") as f:
                        f.write(text)                            
            except Exception as e:
                print("An error occurred: {}".format(e))

if __name__ == "__main__":
    main()

