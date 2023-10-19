class QuestionService:
    def json(question):
        return {'id': question.id, 'question': question.question}