class QuestionModel:
    def __init__(self,id,question):
        #START TEXT TO SPEECH AS engine
        self.id = id
        self.question = question
    
    def getId(self):
        return self.id
    
    def getQuestion(self):
        return self.question