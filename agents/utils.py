import re


def strip_thinking(text: str) -> str:
    """Elimina bloques <think>...</think> que genera qwen3 en modo razonamiento."""
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return cleaned.strip()


def format_history(history: list, max_turns: int = 4) -> str:
    """Formatea el historial reciente de conversación para el prompt."""
    if not history:
        return ""
    recent = history[-(max_turns * 2):]
    lines = ["Conversación previa con el viajero:"]
    for msg in recent:
        role = "Viajero" if msg.get("role") == "user" else "Marco"
        content = msg.get("text", msg.get("content", msg.get("message", "")))
        truncated = content[:300] + "..." if len(content) > 300 else content
        lines.append(f"{role}: {truncated}")
    return "\n".join(lines)
