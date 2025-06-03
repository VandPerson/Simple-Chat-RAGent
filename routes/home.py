# Basic
from datetime import datetime

# Backend
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

# Custom modules
from core.templates import templates
from services import get_user_history



router = APIRouter()



@router.get("/", response_class=HTMLResponse)
def index_page(request: Request):
    chat_messages = get_user_history()
    
    for message in chat_messages:
        message["timestamp"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    context = {"chat_messages": chat_messages}
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=context)