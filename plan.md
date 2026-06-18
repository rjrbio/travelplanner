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