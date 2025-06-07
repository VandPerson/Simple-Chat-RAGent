# Backend
from fastapi import APIRouter

# Custom modules
from schemas import Message, MessageCreate
from services import ChatService



router = APIRouter()

service = ChatService()



@router.post("/api/ask", response_model=Message)
def ask_assistant(message: MessageCreate, include_history: bool = False):
    answer = service.get_answer(message.content, include_history)
    answer = Message(**answer)
    return answer

@router.get("/api/history", response_model=list[Message])
def get_history():
    history = service.get_user_history()
    messages = [Message(**row) for row in history]
    return messages