# schemas.py
from pydantic import BaseModel

class ChatbotSchema(BaseModel):
    user_input: str