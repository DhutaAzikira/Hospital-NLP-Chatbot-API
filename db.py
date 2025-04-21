from sqlmodel import Session, create_engine
from typing import Annotated
from fastapi import Depends

# === Database Connection ===
DATABASE_URL = "mysql+pymysql://duta:sayadhuta@localhost:3306/hospital"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]