from question import QuestionModel
class InterviewModel:
    def __init__(self,id,presentation,closure):
        #START TEXT TO SPEECH AS engine
        self.id = id
        self.presentation = presentation
        self.closure = closure
        self.questions = []
    
    def addQuestion(self, question):
        quest = QuestionModel(question)
        self.questions.append(quest)
    
    def setPresentation(self,presentation):
        self.presentation = presentation
    
    def setClosure(self,closure):
        self.closure = closure
    
    def getId(self):
        return self.id
    
    def getPresentation(self):
        return self.presentation
    
    def getClosure(self):
        return self.closure
    
    def getQuestions(self):
        return self.questions