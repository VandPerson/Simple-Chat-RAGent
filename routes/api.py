# Basic
from typing import List

# Backend
from fastapi import APIRouter

# Custom modules
from schemas import Message, MessageCreate
from services import get_answer, get_user_history



router = APIRouter()



@router.post("/api/ask", response_model=Message)
def ask_assistant(message: MessageCreate, enable_history: bool = False):
    answer = get_answer(message.content, enable_history)
    answer = Message(**answer)
    return answer

@router.get("/api/history", response_model=List[Message])
def get_history():
    history = get_user_history()
    messages = [Message(**row) for row in history]
    return messages