from fastapi import APIRouter, HTTPException
from db import SessionDep
from sqlmodel import select
from models.models import Doctors, WeeklySchedule, Appointments


router = APIRouter()

@router.get("/doctors")
async def get_doctors(session: SessionDep):
    try:
        statement = select(Doctors)
        doctors = session.exec(statement).all()
        return doctors

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")