# routes/chatbot_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Annotated

from intent_classifier import intent_classifier
from intent_handlers._intent_router import intent_map
from db import get_session
from schemas.ChatbotSchema import ChatbotSchema

router = APIRouter()
SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/chatbot")
def handle_user_input(request: ChatbotSchema, session: SessionDep):
    user_input = request.user_input
    intent = intent_classifier.classify(user_input)

    handler = intent_map.get(intent)

    if handler:
        try:
            response = handler(session, user_input)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Handler error: {str(e)}")
    else:
        response = "Sorry, I can't handle that yet."

    return {"intent": intent, "response": response}
