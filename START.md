**START — feature/backend**

- **Propósito:** Poner en marcha la rama `feature/backend` y dejar instrucciones mínimas para comenzar a implementar los endpoints del backend.

- **Checklist rápida:**
  - Hacer `git pull origin feature/backend` para sincronizar.
  - Crear y activar entorno virtual: `python -m venv .venv` → `.\\.venv\\Scripts\\Activate.ps1`.
  - `pip install -r requirements.txt`.
  - Ejecutar la app: `uvicorn backend.main:app --reload --port 8000`.

- **Endpoints a implementar / mejorar (archivo sugerido):**
  - `/plan` — [backend/api/plan.py](backend/api/plan.py) : implementar lógica real o mocks mejorados.
  - `/search` — [backend/api/search.py](backend/api/search.py) : integrar con `integrations/` o mock.
  - `/itinerary` — [backend/api/itinerary.py](backend/api/itinerary.py).

- **Tareas iniciales (prioridad):**
  1. Añadir validaciones de entrada y models pydantic en `backend/api/*`.
  2. Implementar servicio de flights mock en `integrations/flights/*` y conectarlo al endpoint `search`.
  3. Añadir tests unitarios básicos en `tests/test_api.py` (marcar los endpoints nuevos).

- **Comprobaciones locales:**
  - `curl http://localhost:8000/health` → debe devolver OK.
  - Ejecutar tests locales: `pytest tests/test_api.py::test_health -q` (si `pytest` instalado).

- **Notas de colaboración:**
  - Abrir PR desde `feature/backend` a `develop` o `main` cuando completes una tarea funcional mínima.
  - Referenciar la issue correspondiente y asignar revisores.
