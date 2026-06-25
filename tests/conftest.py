import pytest


def ollama_disponible() -> bool:
    try:
        import requests
        r = requests.get("http://localhost:11434/api/tags", timeout=2)
        return r.status_code == 200
    except Exception:
        return False


def modelo_disponible() -> bool:
    if not ollama_disponible():
        return False
    try:
        import requests
        r = requests.post(
            "http://localhost:11434/api/show",
            json={"name": "qwen3:1.7b"},
            timeout=2,
        )
        return r.status_code == 200
    except Exception:
        return False


pytestmark_agentes = pytest.mark.skipif(
    not modelo_disponible(),
    reason="Requiere Ollama con modelo qwen3:1.7b (ollama pull qwen3:1.7b)",
)
