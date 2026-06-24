from fastapi import APIRouter
from api.schemas.chat_schema import ChatRequest
from api.deps.session_manager import SessionManager

router = APIRouter()

@router.post("/{session_id}")
def chat(session_id: str, request: ChatRequest):

    # Guardar mensaje del usuario
    SessionManager.append_message(session_id, "user", request.message)

    # RESPUESTA SIMULADA (sin grafo)
    bot_response = f"Simulación de respuesta para: {request.message}"

    # Guardar respuesta del bot
    SessionManager.append_message(session_id, "bot", bot_response)

    return {"response": bot_response}
