from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers.user_controller import router as user_router
from controllers.interview_controller import router as interview_router
from controllers.question_controller import router as question_router
from controllers.history_controller import router as history_router
from configurations.config import settings

app = FastAPI()

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up routes
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(interview_router, prefix="/interviews", tags=["interviews"])
app.include_router(question_router, prefix="/questions", tags=["questions"])
app.include_router(history_router, prefix="/histories", tags=["histories"])