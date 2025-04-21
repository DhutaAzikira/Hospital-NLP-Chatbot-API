from sqlmodel import SQLModel, Field
# === models ===
class Doctors(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    specialty: str
    phone: str
    email: str

class Patients(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    age: int
    phone: str
    email: str
    doctor_id: int = Field(foreign_key="doctors.id")

class WeeklySchedule(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    doctor_id: int = Field(foreign_key="doctors.id")
    day: str
    time: str

class Appointments(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patients.id")
    doctor_id: int = Field(foreign_key="doctors.id")
    date: str
    time: str
