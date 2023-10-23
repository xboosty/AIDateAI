from fastapi import APIRouter, HTTPException
from typing import List
from dto.interview_dto import InterviewDto
from persistence.interview_repository import InterviewRepository
from configurations.config import get_db as async_session
from services.interview_service import InterviewService

router = APIRouter()
interview_repository = InterviewRepository(async_session())
interview_service = InterviewService(interview_repository)

@router.post("/interviews")
async def create_interview(interview_dto: InterviewDto):
    try:
        interview = interview_service.create_interview(interview_dto)
        return interview
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/interviews")
async def read_interviews():
    try:
        interviews = interview_service.read_interviews()
        return interviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/interviews/{interview_id}")
async def read_interview(interview_id: int):
    try:
        interview = interview_service.read_interview(interview_id)
        if interview is None:
            raise HTTPException(status_code=404, detail="Interview not found")
        return interview
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/interviews/{interview_id}")
async def update_interview(interview_id: int, interview_dto: InterviewDto):
    try:
        interview = interview_service.update_interview(interview_id, interview_dto)
        if interview is None:
            raise HTTPException(status_code=404, detail="Interview not found")
        return interview
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/interviews/{interview_id}")
async def delete_interview(interview_id: int):
    try:
        interview = interview_service.delete_interview(interview_id)
        if interview is None:
            raise HTTPException(status_code=404, detail="Interview not found")
        return interview
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))