import pyttsx3

class Speaker:
    def __init__(self):
        #START TEXT TO SPEECH AS engine
        self.engine = pyttsx3.init()
    
    def speak_text(self, text):
        self.engine.say(text)
        self.engine.runAndWait()