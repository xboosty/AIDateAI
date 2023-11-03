from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.transcription_routes import router_transcription
from routes.user_routes import router_user
from routes.interview_routes import router_interview
from routes.question_routes import router_question
from routes.history_routes import router_history
from routes.security import router_security
from configurations.config import settings

app = FastAPI(
        title = "My FastAPI for AI Module",
        description = "A REST API built with FastAPI for AI Module.",
        version = "1.0.0",
    )


# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Set up routes
app.include_router(router_transcription, prefix="/ai/transcriptions", tags=["transcriptions"])
app.include_router(router_user, prefix="/users", tags=["users"])
app.include_router(router_interview, prefix="/interviews", tags=["interviews"])
app.include_router(router_question, prefix="/questions", tags=["questions"])
app.include_router(router_history, prefix="/histories", tags=["histories"])
app.include_router(router_security, prefix="/security", tags=["security"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)