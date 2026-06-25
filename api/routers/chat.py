import logging
import re

from fastapi import APIRouter, HTTPException

from api.schemas.chat_schema import ChatRequest
from api.deps.session_manager import SessionManager

logger = logging.getLogger(__name__)
router = APIRouter()


def _mock_response(destino: str, dias: int) -> str:
    return (
        f"## {destino} — {dias} días\n\n"
        f"Plan para {dias} días en {destino}. "
        "Consulta vuelos, actividades y más.\n\n"
        "### Opciones sugeridas\n"
        f"- Vuelo a {destino} desde €150\n"
        f"- Hotel en {destino} desde €60/noche\n"
        f"- Tour guiado por {destino} €40\n\n"
        "### Itinerario\n"
        + "\n".join(
            f"- Día {i+1}: Exploración en {destino}"
            for i in range(dias)
        )
    )


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
            parts = [f"- **{name}**" if name else ""]
            if desc:
                parts.append(f"  {desc[:120]}")
            if precio or rating:
                extra = "  " + " · ".join(filter(None, [
                    f"€{precio}" if precio else "",
                    f"⭐ {rating}" if rating else "",
                ]))
                parts.append(extra)
            lines.append("\n".join(parts))
        else:
            lines.append(f"- {a}")
    return "\n".join(lines)


def _format_itinerario(itinerario: dict, destino: str, dias: int) -> str:
    if not itinerario or not itinerario.get("days"):
        return "\n".join(f"- Día {i+1}: Exploración en {destino}" for i in range(dias))

    lines = ["\n### Itinerario\n"]
    for dia in itinerario["days"]:
        if isinstance(dia, dict):
            titulo = dia.get("title", dia.get("nombre", f"Día"))
            desc = dia.get("description", dia.get("descripcion", ""))
            acts = dia.get("suggested_activities", [])
            lines.append(f"#### {titulo}")
            if desc:
                lines.append(f"{desc}")
            if acts:
                for act in acts[:3]:
                    if isinstance(act, dict):
                        lines.append(f"- {act.get('name', act.get('nombre', ''))}")
                    else:
                        lines.append(f"- {act}")
            lines.append("")
        else:
            lines.append(f"- {dia}")

    extras = []
    if itinerario.get("tips"):
        extras.append(f"\n**Consejos:** {' '.join(itinerario['tips'][:3])}")
    if itinerario.get("weather"):
        extras.append(f"**Clima:** {itinerario['weather'][:200]}")
    if extras:
        lines.append("\n".join(extras))

    return "\n".join(lines)


def _extract_destination(message: str) -> str | None:
    stop_words = {"para", "por", "durante", "en", "de", "con", "desde",
                  "hasta", "un", "una", "el", "la", "los", "las", "del"}
    patrones = [
        r"(?:viajar\s+a|visit(?:ar)?\s+|ir\s+a|destino\s+)\s*(.+?)(?=\s+(?:para|por|durante|en|de|con|desde|hasta)\s|\s*\d|\Z)",
        r"\b(?:a|hacia)\s+(.+?)(?=\s+(?:para|por|durante|en|de|con)\s|\s*\d|\Z)",
    ]
    for pat in patrones:
        match = re.search(pat, message, re.IGNORECASE)
        if match:
            raw = match.group(1).strip()
            parts = raw.split()
            filtered = [p for p in parts if p.lower() not in stop_words]
            if filtered:
                return " ".join(filtered).title()

    words = message.split()
    capitalized = []
    question_words = {"qué", "que", "quien", "quienes", "cual", "cuales",
                      "como", "cómo", "donde", "dónde", "cuando", "cuándo",
                      "dame", "necesito", "quiero", "busco", "información"}
    for w in words:
        w_clean = w.strip(",.!?¿¡:;")
        if w_clean[0:1].isupper() and w_clean.lower() not in stop_words | question_words:
            capitalized.append(w_clean)
    if capitalized:
        result = " ".join(capitalized)
        words_clean = [w for w in result.split() if not w.isdigit()]
        return " ".join(words_clean) if words_clean else None

    for w in reversed(words):
        w_clean = w.strip(",.!?¿¡")
        if len(w_clean) >= 3 and w_clean.lower() not in stop_words:
            return w_clean.title()
    return None


def _extract_days(message: str) -> int:
    match = re.search(r"(\d+)\s*(?:d[ií]as|d[ií]a)", message, re.IGNORECASE)
    return int(match.group(1)) if match else 3


@router.post("/{session_id}")
def chat(session_id: str, request: ChatRequest):
    if not SessionManager.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Sesión no encontrada")
    SessionManager.append_message(session_id, "user", request.message)

    destino = _extract_destination(request.message)
    dias = _extract_days(request.message)

    if not destino:
        bot_response = (
            "No entendí bien el destino. "
            "Por favor escribe algo como: "
            '"Quiero viajar a París por 5 días"'
        )
    else:
        try:
            from graph.graph import ejecutar_viaje
            resultado = ejecutar_viaje(destino, dias)
            plan = resultado.get("mensaje_motivacional", "")
            atracciones = resultado.get("opciones_busqueda", [])
            itinerario = resultado.get("itinerario", {})

            bot_response = f"## {destino} — {dias} días\n\n"
            bot_response += f"{plan}\n"
            bot_response += _format_attractions(atracciones)
            bot_response += _format_itinerario(itinerario, destino, dias)
        except Exception:
            logger.exception("Graph failed for session %s dest=%s", session_id, destino)
            bot_response = _mock_response(destino, dias)

    SessionManager.append_message(session_id, "bot", bot_response)
    return {"response": bot_response}
