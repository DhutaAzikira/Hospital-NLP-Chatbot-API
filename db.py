import os
from dotenv import load_dotenv
from sqlmodel import Session, create_engine
from typing import Annotated
from fastapi import Depends

load_dotenv()

# === Database Connection ===
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={
        "ssl_ca": "certs/ca.pem",  # Full path to your CA cert
        "ssl_verify_cert": True         # Enforce SSL certificate validation
    }
)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]