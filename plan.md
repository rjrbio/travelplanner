# Plan simplificado y objetivo MVP

## Objetivo
Reducir el alcance a un MVP realizable en pocas jornadas por desarrollador, enfocando en pruebas de integración y funcionalidad mínima.

## MVP mínimo (prioridad)
- Endpoints básicos en el backend: `/plan` y `/search` (respuesta mock/estructurada).
- `Planner Agent`: generación básica de plan (reglas simples o prompts cortos).
- `Search Agent`: devuelve opciones mock de vuelos/hoteles/tours.
- RAG mínimo: vector store local con ingestión simple (opcional para sprint 1).
- Docker + `.env.example` para reproducibilidad.

## Roles condensados y entregables (mínimos)

### Dev 1 — Backend (8–16h)
- Implementar `backend/main.py` con `/plan` y `/search` (mock responses).
- Dockerfile, `docker-compose.yml` y `.env.example`.
- Criterio de aceptación: endpoints responden con JSON válido.

### Dev 2 — Agentes (8–16h)
- Implementar `Planner Agent` y `Search Agent` con lógica simple (no integraciones externas aún).
- Documentar prompts básicos en `/prompts/`.
- Criterio de aceptación: agentes devuelven estructura esperada y hay tests unitarios básicos.

### Dev 3 — RAG & Integraciones (prioridad baja, 8–24h)
- Inicialmente usar un vectorstore local (placeholder) y permitir ingestión de textos.
- Postergar integraciones reales (Amadeus, Booking, etc.) y usar mocks hasta que MVP esté estable.
- Criterio de aceptación: ingestión y búsqueda simple funcionan con documentos de ejemplo.

## Ramas sugeridas (simplicidad)
- `feature/backend` (Dev 1)
- `feature/agents` (Dev 2)
- `feature/rag-mock` (Dev 3)

## Flujo de trabajo recomendado
- Cada dev trabaja en su rama temática y abre PRs cortos hacia `develop`.
- Revisiones rápidas (1 reviewer) y merges frecuentes.
- Entregables pequeños y verificables: 1 PR = 1 funcionalidad mínima.

## Estimación de tiempo (por dev)
- Sprint corto (2–3 días de trabajo enfocado / 16–24 horas). Objetivo: tener un demo interno al final.

## Criterios de aceptación del MVP
1. `GET /plan` devuelve plan con campos `destination`, `days`, `summary`.
2. `GET /search` devuelve lista de opciones (mínimo 2).
3. Agentes básicos integrados con backend (llamadas internas o mocks).
4. Proyecto se inicia con `docker-compose up` (documentado).

## Siguientes pasos (prioritarios)
1. Asignar quién implementa cada rama y bloquear 1–2 días para el MVP.
2. Lanzar PRs pequeños y celebrar una demo interna.
3. Si MVP estable, planificar integraciones externas y mejoras (LangGraph, Ollama, paralelización).

---
Este plan reduce complejidad, elimina integraciones externas en la fase inicial y prioriza entrega rápida y verificable.

## Instrucciones paso a paso por desarrollador

Las siguientes tareas están pensadas para que cada desarrollador pueda trabajar de forma independiente en su rama y entregar pequeñas PRs verificables.

### Dev 1 — Backend (rama: `feature/backend`) (8–16h)
Paso a paso
1. Crear/activar entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Implementar endpoints mínimos en `backend/main.py` y `backend/api/`:
	- `GET /plan?destination=...&days=...` → devuelve JSON con `destination`, `days`, `summary`.
	- `GET /search?query=...` → devuelve lista corta de opciones mock.

3. Añadir tests rápidos en `tests/test_api.py` (ej.: `TestClient` de FastAPI).

4. Añadir `Dockerfile` y `docker-compose.yml` para levantar el servicio localmente.

5. Verificación local:

```powershell
uvicorn backend.main:app --reload --port 8000
curl "http://localhost:8000/plan?destination=Madrid&days=3"
pytest -q tests/test_api.py
```

6. PR checklist (pequeño PR):
	- Endpoints responden correctamente.
	- Tests pasan localmente.
	- `Dockerfile` construye la imagen mínima.

### Dev 2 — Agentes (rama: `feature/agents`) (8–16h)
Paso a paso
1. Implementar `agents/planner_agent.py` y `agents/search_agent.py` con funciones públicas claras:
	- `planner_agent.plan_trip(destination, days) -> dict`
	- `search_agent.search_options(query) -> list`

2. Mantener lógica simple: reglas basadas en plantillas o llamadas a LLMs locales later; por ahora usar mocks o reglas heurísticas.

3. Crear prompts básicos en `prompts/` y añadir un pequeño README explicando cómo probar cada prompt.

4. Tests unitarios en `tests/test_agents.py` que validen estructura de salida.

5. Integración con backend (Dev 1): exponer una función interna o endpoint opcional que llame al agente para devolución inmediata en demo.

6. Verificación:

```powershell
python -c "from agents.planner_agent import PlannerAgent; print(PlannerAgent().plan_trip('Roma',3))"
pytest -q tests/test_agents.py
```

7. PR checklist:
	- Agentes devuelven JSON con formato esperado.
	- Tests unitarios pasan.
	- Documentación mínima en `/prompts/`.

### Dev 3 — RAG & Mocks de Integraciones (rama: `feature/rag-mock`) (8–24h)
Paso a paso
1. Revisar el ejemplo `ej-chroma_persistente.py` como referencia de ingestión y búsqueda (usa `chroma_db` persistente y `docs/` para PDFs).

2. Implementar un módulo mínimo `rag/ingest.py` con:
	- Función `ingest_folder(path: str)` que crea chunks y los añade a `Chroma` o a un `VectorStore` placeholder.
	- Uso de ids deterministas para reindexar sin duplicar.

3. Proveer un script de prueba `ej-chroma_persistente.py` (ya existe) y documentar cómo ejecutarlo:

```powershell
python ej-chroma_persistente.py
```

4. Si Chroma/embeddings no están disponibles localmente, usar un `VectorStore` en memoria con embeddings dummy (longitud del texto, etc.) para las pruebas.

5. Tests:
	- Test de ingestión que verifique que `store.search()` devuelve resultados para una consulta conocida.

6. PR checklist:
	- Script de ingestión funciona con documentos de ejemplo en `docs/`.
	- Búsqueda devuelve resultados y metadatos útiles (`source`, `page`).

## Contratos mínimos entre componentes
- `GET /plan` acepta `destination` y `days` y devuelve `destination`, `days`, `summary`.
- `GET /search` acepta `query` y devuelve `results: list[str]` o `results: list[dict]`.
- Los agentes exponen funciones que el backend puede importar y ejecutar (evitar llamadas remotas en MVP).

## Checklist de PRs y demo
- Cada PR debe ser pequeña (máx. 1–3 archivos modificados por funcionalidad).
- Incluir tests que cubran casos felices y un caso de error simple.
- Demo mínimo: arrancar `docker-compose up` y ejecutar dos llamadas: `/plan` y `/search`.

---
Si quieres, procedo a: (A) crear ramas `feature/backend`, `feature/agents`, `feature/rag-mock` en el remoto y (B) commitear y pushear este `plan.md` actualizado. ¿Cuál prefieres? 