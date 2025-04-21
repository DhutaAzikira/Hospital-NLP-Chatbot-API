from sqlmodel import Session, select
from models.models import Doctors, WeeklySchedule

def handle_doctor_schedule(session: Session, user_input: str):
    statement = select(Doctors, WeeklySchedule).join(WeeklySchedule)
    results = session.exec(statement)

    return [
        {
            "doctor_name": doctor.name,
            "specialty": doctor.specialty,
            "day": schedule.day,
            "time": schedule.time,
        }
        for doctor, schedule in results
    ]