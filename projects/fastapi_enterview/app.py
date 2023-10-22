from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.user_controller import UserController
from controllers.interview_controller import InterviewController
from controllers.question_controller import QuestionController
from controllers.history_controller import HistoryController
from config import settings

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up controllers
user_controller = UserController()
interview_controller = InterviewController()
question_controller = QuestionController()
history_controller = HistoryController()

# Set up routes
app.include_router(user_controller.router, prefix="/users", tags=["users"])
app.include_router(interview_controller.router, prefix="/interviews", tags=["interviews"])
app.include_router(question_controller.router, prefix="/questions", tags=["questions"])
app.include_router(history_controller.router, prefix="/histories", tags=["histories"])