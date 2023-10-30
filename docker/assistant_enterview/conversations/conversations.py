from .speaks.speak_text import Speaker

class Conversation:
    
    def __init__(self,presentation,questions):
        #START TEXT TO SPEECH AS engine
        self.presentation = presentation
        self.questions = questions
        self.speaker = Speaker()
        
    def setPresentation(self, newPresentation):
        self.presentation = newPresentation
        with open("presentation.txt","w") as f:
            f.write(self.presentation)
        
    def getPresentation(self):
        with open("presentation.txt","r") as f:
            text = f.read()
        return text
        
    def setQuestions(self, newQuestions):
        self.questions = newQuestions
    
    def speakPresentation(self):
        with open("presentation.txt","r") as f:
            text = f.read()
        self.speaker.speak_text(text)
        
    def getQuestions(self):
        return self.questions
    
    def speakQuestion(self, position):
        self.speaker.speak_text(self.questions[position])
        
    def speakAny(self, message):
        self.speaker.speak_text(message)