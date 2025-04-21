# intent_handlers/book_appointment.py
from sqlmodel import Session, select
from models.models import Doctors, Appointments, Patients
import re
import dateparser

DOCTOR_MAP = {
    "aisha": "Dr. Aisha Khan",
    "liam": "Dr. Liam Carter",
    "nora": "Dr. Nora Lin"
}

def extract_doctor_name(user_input: str) -> str | None:
    user_input_lower = user_input.lower()
    for key in DOCTOR_MAP:
        if key in user_input_lower:
            return DOCTOR_MAP[key]
    return None

def extract_datetime(user_input: str):
    # Common time expressions: "at 9:00", "09:00", "9am", "Monday 10am", etc.
    time_patterns = [
        r"(?:on\s+)?(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)?\s*(?:at\s*)?\d{1,2}(?::\d{2})?\s*(?:am|pm)?",  # e.g., "Monday 09:00"
        r"(?:tomorrow|today|next\s+\w+)\s*(?:at\s*)?\d{1,2}(?::\d{2})?\s*(?:am|pm)?",  # "tomorrow at 10am"
        r"\d{1,2}(?::\d{2})?\s*(?:am|pm)?",  # "9:00", "9am"
    ]

    combined_pattern = "|".join(time_patterns)
    matches = re.findall(combined_pattern, user_input.lower())

    for match in matches:
        cleaned = match.strip()
        parsed = dateparser.parse(cleaned)
        if parsed:
            return parsed.strftime("%Y-%m-%d"), parsed.strftime("%H:%M")

    # Fallback to parsing full sentence
    parsed = dateparser.parse(user_input)
    if parsed:
        return parsed.strftime("%Y-%m-%d"), parsed.strftime("%H:%M")

    return None, None

def handle_book_appointment(
    session: Session,
    user_input: str,
    step: str = "get_doctor_time",
    partial_data: dict = None,
    default_patient_id: int = 1
) -> tuple[str, str, dict]:
    if partial_data is None:
        partial_data = {}

    if step == "get_doctor_time":
        doctor_name = extract_doctor_name(user_input)
        date, time = extract_datetime(user_input)

        if not doctor_name:
            return "Which doctor would you like to book an appointment with?", "get_doctor_time", partial_data

        if not time:
            return f"What time would you like to book your appointment with {doctor_name}?", "get_doctor_time", {"doctor_name": doctor_name}

        partial_data.update({
            "doctor_name": doctor_name,
            "date": date,
            "time": time,
            "patient_id": default_patient_id  # ← Hardcoded patient
        })
        return handle_book_appointment(session, "", step="finalize", partial_data=partial_data)

    elif step == "finalize":
        doctor = session.exec(select(Doctors).where(Doctors.name == partial_data["doctor_name"])).first()
        if not doctor:
            return f"Sorry, I couldn't find a doctor named {partial_data['doctor_name']}.", "get_doctor_time", {}

        appointment = Appointments(
            patient_id=partial_data["patient_id"],
            doctor_id=doctor.id,
            date=partial_data["date"],
            time=partial_data["time"]
        )
        session.add(appointment)
        session.commit()

        return f"Appointment successfully booked with {doctor.name} on {partial_data['date']} at {partial_data['time']}.", "complete", {}

