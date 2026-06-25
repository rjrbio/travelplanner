import logging
import os
import re

from fastapi import APIRouter, HTTPException
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

from api.chat_schema import ChatRequest
from api.deps.session_manager import SessionManager
from agents.utils import strip_thinking, format_history

logger = logging.getLogger(__name__)
router = APIRouter()

OLLAMA_URL = os.getenv("OLLAMA_API_BASE_URL", "http://localhost:11434")


# ─── Helpers de extracción ────────────────────────────────────────────────────

def _extract_destination(message: str) -> str | None:
    stop_words = {"para", "por", "durante", "en", "de", "con", "desde",
                  "hasta", "un", "una", "el", "la", "los", "las", "del"}
    patrones = [
        r"(?:viajar\s+a|visit(?:ar)?\s+|ir\s+a|destino\s+|viaje\s+a)\s*(.+?)(?=\s+(?:para|por|durante|de|con|desde|hasta)\s|\s*\d|\Z)",
        r"\b(?:a|hacia)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñA-ZÁÉÍÓÚÑ\s]{2,30})(?=\s+(?:para|por|durante|en|\d)|\Z)",
    ]
    for pat in patrones:
        match = re.search(pat, message, re.IGNORECASE)
        if match:
            raw = match.group(1).strip()
            parts = raw.split()
            filtered = [p for p in parts if p.lower() not in stop_words]
            if filtered:
                return " ".join(filtered[:3]).title()

    words = message.split()
    question_words = {"qué", "que", "quien", "quienes", "cual", "cuales",
                      "como", "cómo", "donde", "dónde", "cuando", "cuándo",
                      "dame", "necesito", "quiero", "busco", "información",
                      "tengo", "hay", "puedo", "debo", "vale", "hola"}
    capitalized = [
        w.strip(",.!?¿¡:;") for w in words
        if w.strip(",.!?¿¡:;")[:1].isupper()
        and w.strip(",.!?¿¡:;").lower() not in stop_words | question_words
        and not w.strip(",.!?¿¡:;").isdigit()
    ]
    if capitalized:
        return " ".join(capitalized[:3])

    return None


def _extract_days(message: str) -> int:
    match = re.search(r"(\d+)\s*(?:d[ií]as?|semanas?)", message, re.IGNORECASE)
    if match:
        val = int(match.group(1))
        if "semana" in match.group(0).lower():
            val *= 7
        return max(1, min(val, 30))
    return 3


def _is_trip_request(message: str) -> bool:
    """Determina si el mensaje es una solicitud de planificación de viaje."""
    trip_keywords = [
        r"viajar\s+a", r"ir\s+a", r"visitar\s+", r"viaje\s+a",
        r"\d+\s*d[ií]as?", r"semanas?\s+en", r"planif",
        r"itinerario", r"quiero\s+ir", r"quiero\s+viajar",
    ]
    msg_lower = message.lower()
    return any(re.search(kw, msg_lower) for kw in trip_keywords)


_DESTINOS_FUERA_ESPANA = {
    # Ciudades internacionales frecuentes
    "paris", "parís", "roma", "rome", "london", "londres",
    "tokio", "tokyo", "nueva york", "new york", "berlin", "berlín",
    "amsterdam", "dubai", "bangkok", "sydney", "buenos aires",
    "ciudad de mexico", "ciudad de méxico", "mexico", "méxico",
    "miami", "los angeles", "chicago", "toronto", "moscu", "moscú",
    "beijing", "pekín", "pekin", "shanghai", "hong kong",
    "singapur", "singapore", "cairo", "el cairo", "nairobi",
    "marrakech", "marrakesh", "lisboa", "lisbon", "oporto", "porto",
    "niza", "nice", "venecia", "venice", "florencia", "florence",
    "milan", "milán", "napoles", "nápoles", "naples",
    "viena", "vienna", "praga", "prague", "budapest",
    "varsovia", "warsaw", "estocolmo", "stockholm", "oslo",
    "copenhague", "copenhagen", "helsinki", "dublin", "edimburgo",
    "edinburgh", "atenas", "athens", "estambul", "istanbul",
    "rio de janeiro", "río de janeiro", "sao paulo", "são paulo",
    "bogota", "bogotá", "lima", "santiago", "caracas",
    "nueva delhi", "new delhi", "mumbai", "bombay",
    "kuala lumpur", "jakarta", "manila", "seul", "seúl", "seoul",
    # Países completos cuando se mencionan como destino
    "japon", "japón", "china", "india", "brasil", "brazil",
    "argentina", "colombia", "chile", "peru", "perú",
    "marruecos", "morocco", "egipto", "egypt",
    "tailandia", "thailand", "indonesia", "vietnam",
    "estados unidos", "usa", "reino unido", "uk",
    "alemania", "germany", "francia", "france",
    "italia", "italy", "portugal", "holanda", "netherlands",
    "belgica", "bélgica", "belgium", "suiza", "switzerland", "austria",
    "grecia", "greece", "turquia", "turquía", "turkey",
    "canada", "australia", "nueva zelanda", "new zealand",
    "sudafrica", "sudáfrica", "south africa", "nigeria", "kenya",
}


def _es_destino_espanol(destination: str) -> bool:
    """Devuelve False si el destino está claramente fuera de España."""
    return destination.lower().strip() not in _DESTINOS_FUERA_ESPANA


# ─── Respuesta conversacional (sin destino claro) ────────────────────────────

def _conversational_response(user_message: str, history: list) -> str:
    try:
        llm = ChatOllama(
            model="qwen3:1.7b",
            temperature=0.7,
            num_predict=512,
            base_url=OLLAMA_URL,
            client_kwargs={"timeout": 60},
        )
        with open("prompts/conversational.txt", "r", encoding="utf-8") as f:
            prompt_text = f.read()

        history_text = format_history(history, max_turns=3)
        history_section = history_text if history_text else ""

        prompt = ChatPromptTemplate.from_template(prompt_text)
        chain = prompt | llm
        response = chain.invoke({
            "user_message": user_message,
            "history_section": history_section,
        })
        return strip_thinking(response.content)
    except Exception:
        logger.exception("Error en respuesta conversacional")
        return (
            "¡Hola! Soy Marco, tu consultor de viajes. "
            "Cuéntame a dónde quieres ir y cuántos días tienes, "
            "y te preparo un itinerario personalizado."
        )


# ─── Formateadores de respuesta ───────────────────────────────────────────────

def _format_attractions(atracciones: list) -> str:
    if not atracciones:
        return ""
    lines = ["\n### Atracciones destacadas\n"]
    for a in atracciones[:5]:
        if isinstance(a, dict):
            name = a.get("name", a.get("nombre", ""))
            desc = a.get("description", a.get("descripcion", ""))
            precio = a.get("price", a.get("precio", ""))
            rating = a.get("rating", "")
            if not name:
                continue
            line = f"- **{name}**"
            if desc:
                line += f" — {desc[:100]}"
            extras = " · ".join(filter(None, [
                f"€{precio}" if precio else "",
                f"⭐ {rating}" if rating else "",
            ]))
            if extras:
                line += f" ({extras})"
            lines.append(line)
        else:
            lines.append(f"- {a}")
    return "\n".join(lines) if len(lines) > 1 else ""


def _format_itinerario(itinerario: dict, destino: str, dias: int) -> str:
    if not itinerario or not itinerario.get("days"):
        return ""

    lines = ["\n### Itinerario día a día\n"]
    for i, dia in enumerate(itinerario["days"], 1):
        if not isinstance(dia, dict):
            lines.append(f"- Día {i}: {dia}")
            continue

        titulo = dia.get("title", f"Día {i} en {destino}")
        desc = dia.get("description", "")
        acts = dia.get("suggested_activities", [])

        lines.append(f"#### Día {i}: {titulo}")
        if desc:
            lines.append(desc)
        if acts:
            for act in acts[:3]:
                name = act.get("name", act) if isinstance(act, dict) else act
                lines.append(f"- {name}")
        lines.append("")

    return "\n".join(lines)


# ─── Endpoint principal ───────────────────────────────────────────────────────

@router.post("/{session_id}")
def chat(session_id: str, request: ChatRequest):
    if not SessionManager.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    SessionManager.append_message(session_id, "user", request.message)

    history = SessionManager.get_history(session_id)

    destino = _extract_destination(request.message)
    dias = _extract_days(request.message)
    is_trip = _is_trip_request(request.message)

    if destino and is_trip and not _es_destino_espanol(destino):
        bot_response = (
            f"Lo siento, solo puedo ayudarte a planificar viajes por **España**. "
            f"{destino} queda fuera de mi área de especialización. "
            f"¿Te animas a descubrir algún destino español? "
            f"Puedo prepararte un itinerario para Madrid, Barcelona, Sevilla, Granada, Valencia, "
            f"San Sebastián, Bilbao, Málaga, Toledo, Salamanca y muchos más rincones increíbles de España."
        )
    elif not destino or (not is_trip and len(request.message.split()) < 4):
        bot_response = _conversational_response(request.message, history[:-1])
    else:
        try:
            from graph.graph import ejecutar_viaje
            resultado = ejecutar_viaje(destino, dias, conversation_history=history[:-1])

            plan = resultado.get("mensaje_motivacional", "")
            atracciones = resultado.get("opciones_busqueda", [])
            itinerario = resultado.get("itinerario", {})

            bot_response = f"## {destino} — {dias} {'día' if dias == 1 else 'días'}\n\n"
            if plan:
                bot_response += f"{plan}\n"
            bot_response += _format_attractions(atracciones)
            bot_response += _format_itinerario(itinerario, destino, dias)
        except Exception:
            logger.exception("Graph failed for session %s dest=%s", session_id, destino)
            bot_response = _conversational_response(request.message, history[:-1])

    SessionManager.append_message(session_id, "bot", bot_response)
    return {"response": bot_response}
