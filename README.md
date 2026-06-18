# travelplanner


# 🎯 **Takeaway**
Divide el proyecto en 3 áreas:  
1) **Infraestructura + Backend Core**  
2) **Agentes + LangGraph**  
3) **RAG + Integraciones externas (APIs + mapas)**  

Cada desarrollador tiene ownership claro y ramas dedicadas.

---

# 🧩 1. División del trabajo en 3 desarrolladores

---

# 👨‍💻 **Desarrollador 1 — Backend Core + Infraestructura**
### **Responsabilidades**
- Crear la estructura base del proyecto  
- Configurar Ollama local o remoto  
- Configurar LangGraph (estado, nodos, flujos)  
- Crear API interna (FastAPI o Flask)  
- Manejar variables de entorno y secrets  
- Integrar logging, tracing y manejo de errores  
- Dockerización del proyecto  

### **Entregables**
- Carpeta `/backend/` funcional  
- Servidor API con endpoints:  
  - `/plan`  
  - `/search`  
  - `/itinerary`  
- Dockerfile + docker-compose  
- Configuración de entorno `.env.example`  

### **Ramas sugeridas**
- `feature/backend-core`  
- `feature/api-server`  
- `feature/docker-setup`  

---

# 👩‍💻 **Desarrollador 2 — Agentes + LangGraph**
### **Responsabilidades**
- Implementar los 3 agentes:
  1. Planner Agent  
  2. Search Agent  
  3. Itinerary Builder  
- Crear el grafo en LangGraph  
- Manejar estados y transiciones  
- Integrar los agentes con el backend  
- Crear prompts optimizados para Ollama  
- Implementar paralelización (vuelos/hoteles/tours)  

### **Entregables**
- Carpeta `/agents/`  
- Grafo completo en `/graph/graph.py`  
- Prompts en `/prompts/`  
- Tests unitarios de agentes  

### **Ramas sugeridas**
- `feature/agents-planner`  
- `feature/agents-search`  
- `feature/agents-itinerary`  
- `feature/langgraph-flow`  

---

# 👨‍💻 **Desarrollador 3 — RAG + Integraciones externas (APIs + Mapas)**
### **Responsabilidades**
- Crear la base vectorial (Chroma, Milvus o Qdrant)  
- Implementar embeddings (Nomic, BGE, MPNet)  
- Preparar documentos para RAG (chunking, limpieza)  
- Integrar APIs externas:
  - Amadeus / Skyscanner (vuelos)  
  - Booking / Expedia (hoteles)  
  - Viator / GetYourGuide (tours)  
  - OpenRouteService o Google Maps (distancias)  
- Crear wrappers para cada API  
- Crear el módulo de geocodificación  

### **Entregables**
- Carpeta `/rag/`  
- Carpeta `/integrations/`  
- Scripts de ingestión de documentos  
- Base vectorial inicial  
- Módulo de mapas `/integrations/maps.py`  

### **Ramas sugeridas**
- `feature/rag-setup`  
- `feature/api-integrations`  
- `feature/maps-routing`  

---

# 🗂️ 2. Estructura de carpetas recomendada (GitHub)

```
/project-root
│
├── backend/
│   ├── main.py
│   ├── api/
│   │   ├── plan.py
│   │   ├── search.py
│   │   └── itinerary.py
│   ├── config/
│   │   ├── settings.py
│   │   └── env_loader.py
│   └── utils/
│       ├── logger.py
│       └── errors.py
│
├── agents/
│   ├── planner_agent.py
│   ├── search_agent.py
│   └── itinerary_agent.py
│
├── graph/
│   ├── graph.py
│   └── state.py
│
├── rag/
│   ├── ingest.py
│   ├── vectorstore.py
│   ├── embeddings.py
│   └── documents/
│       ├── europa/
│       ├── asia/
│       ├── america/
│       └── tips/
│
├── integrations/
│   ├── flights/
│   │   ├── amadeus.py
│   │   └── skyscanner.py
│   ├── hotels/
│   │   ├── booking.py
│   │   └── expedia.py
│   ├── tours/
│   │   ├── viator.py
│   │   └── getyourguide.py
│   └── maps/
│       ├── ors.py
│       └── gmaps.py
│
├── prompts/
│   ├── planner.txt
│   ├── search.txt
│   └── itinerary.txt
│
├── tests/
│   ├── test_agents.py
│   ├── test_api.py
│   └── test_rag.py
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# 🏗️ 3. Plan de trabajo por sprints (2 semanas cada uno)

---

## **Sprint 1 — Infraestructura + RAG base**
**Dev 1:**  
- Backend base + API  
- Docker + entorno  

**Dev 2:**  
- Planner Agent  
- Estado inicial en LangGraph  

**Dev 3:**  
- RAG: embeddings + vectorstore  
- Ingesta de documentos  

**Resultado:**  
Proyecto inicial funcionando con un endpoint `/plan`.

---

## **Sprint 2 — Integraciones externas + Agentes**
**Dev 1:**  
- Logging + manejo de errores  
- Configuración de secrets  

**Dev 2:**  
- Search Agent  
- Itinerary Agent  

**Dev 3:**  
- APIs de vuelos, hoteles y tours  
- Mapas (Distance Matrix + geocoding)  

**Resultado:**  
Flujo completo: plan → búsqueda → itinerario.

---

## **Sprint 3 — Optimización + QA**
**Dev 1:**  
- Tests API  
- Optimización de rendimiento  

**Dev 2:**  
- Ajustes de prompts  
- Mejoras en LangGraph  

**Dev 3:**  
- Mejoras en RAG  
- Cache de resultados de APIs  

**Resultado:**  
MVP listo para demo.

