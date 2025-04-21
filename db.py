import os
from dotenv import load_dotenv
from sqlmodel import Session, create_engine
from typing import Annotated
from fastapi import Depends

load_dotenv()

# === Database Connection ===
DATABASE_URL = "mysql://avnadmin:AVNS_A9ZtoDM9GQ7x54SdoYw@hospital-chatbot-service-hospital-chatbot-management.k.aivencloud.com:27086/defaultdb?ssl-mode=REQUIRED"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]