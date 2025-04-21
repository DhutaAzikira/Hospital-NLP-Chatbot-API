# intent_router.py
from intent_handlers.doctor_schedule import handle_doctor_schedule
from intent_handlers.open_hours import handle_open_hours
from intent_handlers.emergency import handle_emergency
from intent_handlers.book_appointment import handle_book_appointment
from intent_handlers.fallback import handle_fallback

intent_map = {
    "doctor_schedule": handle_doctor_schedule,
    "open_hours": handle_open_hours,
    "emergency": handle_emergency,
    "book_appointment": handle_book_appointment,
    "unknown": handle_fallback
}