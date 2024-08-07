from fastapi import APIRouter
from pydantic import BaseModel
from .chat_service import chat_service


chatbot_router = APIRouter()


class ChatRequest(BaseModel):
    user_input: str


@chatbot_router.post("/chat")
async def chat(request: ChatRequest):
    success = False
    response = ""

    try:
        # Request to chat
        response = chat_service(request.user_input)
        success = True
    except Exception as e:
        print(e)

    return {
        "success": success,
        "response": response,
    }
