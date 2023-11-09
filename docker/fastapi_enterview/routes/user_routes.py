from fastapi import APIRouter, HTTPException
from typing import List
from dto.user_dto import UserDtoIn, UserDtoOut
from dto.interview_by_user import InterviewByUserDto
from dto.chat_day_by_user import ChatDayByUserDto
from dto.message_by_user import MessageByUserDto
from configurations.config import get_db
from fastapi.responses import JSONResponse
from fastapi import Depends
from sqlalchemy.orm import Session
from models.user import User
from models.history import History
from models.interview import Interview
from models.question import Question
from sqlalchemy import asc
from datetime import datetime
from .security import oauth2_scheme
import random
import tensorflow as tf
import numpy as np

router_user = APIRouter()

@router_user.get(
    "/users",
    tags=["users"],
    response_model=List[UserDtoOut],
    description="Get a list of all users",
)
def get_users(current_user: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router_user.get(
    "/users/{user_id}",
    tags=["users"],
    response_model=UserDtoOut,
    description="Get a user by ID",
)
def get_user(user_id: int, db: Session = Depends(get_db),current_user: str = Depends(oauth2_scheme)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router_user.get(
    "/users/interviews-by-user/{user_id}",
    tags=["users"],
    response_model=List[InterviewByUserDto],
    description="Get a record of interviews by user ID",
)
def get_interviews_user(user_id: int, db: Session = Depends(get_db),current_user: str = Depends(oauth2_scheme)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    interviews = db.query(Interview).all()
    interviews_data = []  # Lista de entrevistas
    for interview in interviews:
        interviews_data.append(get_percent_and_metadata_interview(user_id, interview.id, db))

    # Devuelve la lista de objetos InterviewByUserDto
    return interviews_data


@router_user.get(
    "/users/by-email/{email}",
    tags=["users"],
    response_model=UserDtoOut,
    description="Get a user by email",
)
def get_user_by_email(email: str, db: Session = Depends(get_db),current_user: str = Depends(oauth2_scheme)):
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router_user.get(
    "/users/compatibility-score/{user_idA}/{user_idB}",
    tags=["users"],
    description="Get compatibility score between  two users",
)
def get_compatibility_score(user_idA: int, user_idB: int, db: Session = Depends(get_db),current_user: str = Depends(oauth2_scheme)):
    offers_A, demands_A, offers_B, demands_B = getvectors_offers_demands(user_idA, user_idB)
    
    model = tf.keras.models.load_model("./ai/models/score_model_with_transferlearning.h5")

    input_vector = np.concatenate([offers_A, demands_A, offers_B, demands_B])

    predicted_percentage = model.predict(np.array([input_vector]))
    predicted_percentage_list = predicted_percentage.tolist()  # Convierte a lista de Python
    return predicted_percentage_list[0][0]


@router_user.post(
    "/users",
    tags=["users"],
    response_model=UserDtoOut,
    description="Create a new user",
)
def create_user(user_create: UserDtoIn, db: Session = Depends(get_db),current_user: str = Depends(oauth2_scheme)):
    user = User(**user_create.dict())  # Crear una instancia de User a partir de los datos del DTO
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router_user.put(
    "/users/{user_id}",
    tags=["users"],
    response_model=UserDtoOut,
    description="Update a user by ID",
)
def update_user(user_id: int, user_update: UserDtoIn, db: Session = Depends(get_db),current_user: str = Depends(oauth2_scheme)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_update.dict().items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

# Eliminar un usuario por ID
@router_user.delete(
    "/users/{user_id}",
    tags=["users"],
    response_model=None,
    description="Delete a user by ID",
)
def delete_user(user_id: int, db: Session = Depends(get_db),current_user: str = Depends(oauth2_scheme)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return JSONResponse(content={"message": "User deleted successfully"}, status_code=204)



#AUXILIARES

# Obtener el historial de un usuario por ID
def get_histories_by_user(user_id: int,interview_id:int, db: Session = Depends(get_db)):
    histories_by_user = db.query(History).filter(History.user_id == user_id, History.interview_id==interview_id).order_by(asc(History.id)).all()
    if histories_by_user is None:
        return []
    
    return histories_by_user
   
   
# Obtener el historial de chat de un usuario por ID y por dias    
def get_chat_days_by_user(user_id: int,interview_id:int, db: Session = Depends(get_db)):
    histories_by_user = get_histories_by_user(user_id,interview_id, db)    
    message_dtos = []
    chat_day_dtos = []
    if histories_by_user.__len__() > 0:
        chat_day = histories_by_user[0].date
        for history in histories_by_user:
            if history.date.date() == chat_day.date():
                message_dtos.append(MessageByUserDto(
                    email=history.user.email,
                    message=history.message,
                    status_message=history.status_message,
                    hour=history.hour,
                    is_bot=not history.is_response,
                    audio="" if history.audio is None else history.audio
                ))
            else:                
                chat_day_dtos.append(ChatDayByUserDto(
                    day=get_days(chat_day),
                    messages=message_dtos
                ))
                chat_day = history.date
                message_dtos = []
                message_dtos.append(MessageByUserDto(
                    email=history.user.email,
                    message=history.message,
                    status_message=history.status_message,
                    hour=history.hour,
                    is_bot=history.is_response,
                    audio="" if history.audio is None else history.audio
                ))
        chat_day_dtos.append(ChatDayByUserDto(
            day=get_days(chat_day),
            messages=message_dtos
        ))
        
    return chat_day_dtos

# Obtener el porcentaje y otros datos de la entrevista de un usuario por ID y por entrevista
def get_percent_and_metadata_interview(user_id: int, interview_id: int, db: Session = Depends(get_db)):
    histories_by_user = db.query(History).filter(History.user_id == user_id, History.interview_id == interview_id).all()
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    questions = db.query(Question).filter(Question.interview_id == interview_id).all()
    
    if interview is None:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    if histories_by_user is None:
        return 0
    
    count = 0
    for history in histories_by_user:
        if history.is_response:
            count = count + 1
    
    return {
                "percent_interview": str(int((count * 100) / questions.__len__()))+"%" if questions.__len__() > 0 else "0%",
                "type_question":', '.join(list(set([question.type for question in questions]))), 
                "title":interview.title, 
                "is_complete":int((count * 100) / questions.__len__())==100 if questions.__len__() > 0 else False,
                "initial_text":interview.initial_text,
                "closure_text":interview.closure_text,
                "historial_chat":get_chat_days_by_user(user_id,interview_id, db)
            }
    
                
        
#Cantidad de días que han pasado desde la fecha de la entrevista    
def get_days(date_to_compare: datetime):        
    today = datetime.now().date()
    diference = today - date_to_compare.date()

    if diference.days == 0:
        return "Today"
    elif diference.days == 1:
        return "Yesterday"
    return date_to_compare.strftime("%d/%m/%Y")

# Obtener los vectores de ofertas y demandas de dos usuarios solo para hardcodear,
# hasta que se implemente la funcionalidad
def getvectors_offers_demands(user_idA, user_idB):    
    offers_A = [random.randint(1, 100) for _ in range(60)]
    demands_A = [random.randint(1, 100) for _ in range(16)]
    offers_B = [random.randint(1, 100) for _ in range(60)]
    demands_B = [random.randint(1, 100) for _ in range(16)]
    return offers_A, demands_A, offers_B, demands_B
    
    
    
    
    