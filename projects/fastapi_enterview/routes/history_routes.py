from fastapi import APIRouter, HTTPException, UploadFile
from typing import List
from dto.history_dto import HistoryDtoIn, HistoryDtoOut
from configurations.config import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from models.history import History
from models.user import User
from models.interview import Interview
from models.question import Question
from fastapi.responses import JSONResponse
from .transcription_routes import model_whisper_medium
from ai.transcription import transcribe_audio_no_delete
import os
from datetime import datetime

router_history = APIRouter()

@router_history.get(
    "/histories",
    tags=["histories"],
    response_model=List[HistoryDtoOut],
    description="Get a list of all histories",
)
def get_histories(db: Session = Depends(get_db)):
    histories = db.query(History).all()
    return histories


@router_history.get(
    "/histories/{history_id}",
    tags=["histories"],
    response_model=HistoryDtoOut,
    description="Get a history by ID",
)
def get_history(history_id: int, db: Session = Depends(get_db)):
    history = db.query(History).filter(History.id == history_id).first()
    if history is None:
        raise HTTPException(status_code=404, detail="History not found")
    return history

@router_history.post(
    "/histories",
    tags=["histories"],
    response_model=HistoryDtoOut,
    description="Create a new history",
)
def create_history(
    #history_create: HistoryDtoIn,
    user_id: int,
    interview_id: int,    
    is_response: bool,
    message: str = None,
    question_id: int = None,
    audio: UploadFile = None,  # Hacer que el audio sea opcional
    db: Session = Depends(get_db)
):
    #history_data = history_create.dict()
    history_data = {
        "user_id": user_id,
        "interview_id": interview_id,
        "message": message,
        "is_response": is_response,
        "question_id": question_id,
        "audio": None,
        "status_message": "SENT",
        "date": datetime.now(),
        "hour": datetime.now().strftime("%H:%M:%S")
    }
    
    user = db.query(User).filter(User.id == history_data['user_id']).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    interview = db.query(Interview).filter(Interview.id == history_data['interview_id']).first()
    if interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    if is_response:
        if history_data['question_id'] is None:
            raise HTTPException(status_code=400, detail="Question ID is required")
        else:
            question = db.query(Question).filter(Question.id == history_data['question_id']).first()
            if question is None:
                raise HTTPException(status_code=404, detail="Question not found")
    else:
        question = None
        audio = None

    # Verifica si se proporcionó un archivo de audio
    if audio is not None:
        path_audio = create_and_save_dir_audio(user, interview, question, audio)
        history_data['audio'] = path_audio
        if history_data['audio'] is None:
            raise HTTPException(status_code=400, detail="Audio file could not be saved")
        try:            
            message = transcribe_audio_no_delete(model_whisper_medium, history_data['audio'])
            history_data['message'] = message
        except Exception as e:
            raise HTTPException(status_code=500, detail="Audio file could not be transcribed")
    else:
        history_data['audio'] = None

    history = History(**history_data)
    
    db.add(history)
    db.commit()
    db.refresh(history)
    
    return history

@router_history.put(
    "/histories/{history_id}",
    tags=["histories"],
    response_model=HistoryDtoOut,
    description="Update a history by ID",
)
def update_history(history_id: int, history_update: HistoryDtoIn, db: Session = Depends(get_db)):
    history = db.query(History).filter(History.id == history_id).first()
    if history is None:
        raise HTTPException(status_code=404, detail="History not found")
    
    for key, value in history_update.dict().items():
        setattr(history, key, value)

    db.commit()
    db.refresh(history)
    return history

# Eliminar un usuario por ID
@router_history.delete(
    "/histories/{history_id}",
    tags=["histories"],
    response_model=None,
    description="Delete a history by ID",
)
def delete_history(history_id: int, db: Session = Depends(get_db)):
    history = db.query(History).filter(History.id == history_id).first()
    if history is None:
        raise HTTPException(status_code=404, detail="History not found")

    db.delete(history)
    db.commit()
    return JSONResponse(content={"message": "History deleted successfully"}, status_code=204)

#AUXILIARES

def create_and_save_dir_audio(user, interview, question, audio):
    username, domain = user.email.split("@")
    subdirectory_name = os.path.join("audios",username+"-"+str(user.id),str(interview.id),str(question.id))
    subdirectory_path = os.path.join(os.getcwd(), subdirectory_name)
    
    if not os.path.exists(subdirectory_path):
        os.makedirs(subdirectory_path)
    
    audio_filename = audio.filename
    audio_path = os.path.join(subdirectory_path, audio_filename)
    
    # Guarda el archivo de audio en el directorio
    with open(audio_path, 'wb') as audio_file:
        audio_file.write(audio.file.read())
    if os.path.exists(audio_path):
        return audio_path
    return None
    