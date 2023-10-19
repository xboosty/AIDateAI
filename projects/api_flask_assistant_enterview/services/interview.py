class InterviewService:
    def json(interview):
        return {'id': interview.id,
                'presentation': interview.presentation,
                'closure': interview.closure,
                'questions': [question.json() for question in interview.questions]
                }
    