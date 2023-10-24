from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user_routes import router_user
from routes.interview_routes import router_interview
from routes.question_routes import router_question
from routes.history_routes import router_history
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
app.include_router(router_user, prefix="/users", tags=["users"])
app.include_router(router_interview, prefix="/interviews", tags=["interviews"])
app.include_router(router_question, prefix="/questions", tags=["questions"])
app.include_router(router_history, prefix="/histories", tags=["histories"])