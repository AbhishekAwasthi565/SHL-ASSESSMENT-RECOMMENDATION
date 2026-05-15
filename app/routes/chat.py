from fastapi import APIRouter
from app.models.schema import ChatRequest, ChatResponse

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    return ChatResponse(
        reply="System initialized.",
        recommendations=[],
        end_of_conversation=False
    )