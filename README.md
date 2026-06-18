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

---

# 🌐 **1. Links oficiales de todas las APIs**

## ✈️ **APIs de Vuelos**
### **1. Amadeus Travel APIs**
[https://developers.amadeus.com](https://developers.amadeus.com)

### **2. Skyscanner API (RapidAPI)**
`https://rapidapi.com/skyscanner/api/skyscanner-flight-search` [(rapidapi.com in Bing)](https://www.bing.com/search?q="https%3A%2F%2Frapidapi.com%2Fskyscanner%2Fapi%2Fskyscanner-flight-search")

### **3. AviationStack**
[https://aviationstack.com](https://aviationstack.com)

---

## 🏨 **APIs de Hoteles**
### **1. Booking.com API (RapidAPI)**
`https://rapidapi.com/apidojo/api/booking` [(rapidapi.com in Bing)](https://www.bing.com/search?q="https%3A%2F%2Frapidapi.com%2Fapidojo%2Fapi%2Fbooking")

### **2. Expedia Rapid API**
[https://developers.expediagroup.com](https://developers.expediagroup.com)

### **3. Amadeus Hotels API**
`https://developers.amadeus.com/self-service/category/hotel` [(developers.amadeus.com in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fdevelopers.amadeus.com%2Fself-service%2Fcategory%2Fhotel")

---

## 🎟️ **APIs de Tours y Actividades**
### **1. Viator API**
[https://www.viator.com/affiliate](https://www.viator.com/affiliate)

### **2. GetYourGuide Partner API**
[https://partner.getyourguide.com](https://partner.getyourguide.com)

### **3. TripAdvisor API (RapidAPI)**
`https://rapidapi.com/apidojo/api/tripadvisor1` [(rapidapi.com in Bing)](https://www.bing.com/search?q="https%3A%2F%2Frapidapi.com%2Fapidojo%2Fapi%2Ftripadvisor1")

---

## 🗺️ **APIs de Mapas, Distancias y Geocodificación**
### **1. OpenRouteService (recomendada)**
`https://openrouteservice.org/dev/#/signup` [(openrouteservice.org in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fopenrouteservice.org%2Fdev%2F%23%2Fsignup")

### **2. Google Maps Platform**
[https://developers.google.com/maps](https://developers.google.com/maps)

### **3. Mapbox**
[https://www.mapbox.com](https://www.mapbox.com)

### **4. OpenStreetMap + Nominatim**
`https://nominatim.org/release-docs/latest/api/Overview/` [(nominatim.org in Bing)](https://www.bing.com/search?q="https%3A%2F%2Fnominatim.org%2Frelease-docs%2Flatest%2Fapi%2FOverview%2F")

---

# 🧠 **2. Diagrama de arquitectura del sistema (texto claro y profesional)**

Aquí tienes un diagrama tipo **arquitectura lógica**, perfecto para documentación o README.

```
                           ┌──────────────────────────┐
                           │        Usuario           │
                           └─────────────┬────────────┘
                                         │
                                         ▼
                           ┌──────────────────────────┐
                           │      Backend API         │
                           │     (FastAPI/Flask)      │
                           └─────────────┬────────────┘
                                         │
                                         ▼
                           ┌──────────────────────────┐
                           │       LangGraph          │
                           │  (Orquestación de LLMs)  │
                           └─────────────┬────────────┘
                                         │
       ┌─────────────────────────────────┼──────────────────────────────────┐
       │                                 │                                  │
       ▼                                 ▼                                  ▼
┌──────────────────┐          ┌──────────────────┐               ┌────────────────────┐
│  Planner Agent   │          │  Search Agent    │               │ Itinerary Builder  │
│ (intención, plan │          │ (APIs externas)  │               │ (RAG + razonamiento│
│   de viaje)      │          │                  │               │   + mapas)         │
└─────────┬────────┘          └─────────┬────────┘               └──────────┬─────────┘
          │                               │                                 │
          │                               │                                 │
          │                               ▼                                 │
          │                 ┌──────────────────────────┐                     │
          │                 │   Integraciones externas  │                     │
          │                 │  (vuelos/hoteles/tours)   │                     │
          │                 └─────────────┬────────────┘                     │
          │                               │                                 │
          │                               ▼                                 │
          │                 ┌──────────────────────────┐                     │
          │                 │      APIs de Mapas       │                     │
          │                 │ (ORS / Google / Mapbox)  │                     │
          │                 └──────────────────────────┘                     │
          │                                                                 │
          ▼                                                                 ▼
┌──────────────────┐                                            ┌──────────────────────────┐
│   Base RAG        │                                            │   Itinerario final       │
│ (vectorstore +    │                                            │ (día a día, costos,      │
│  embeddings)      │                                            │  rutas, recomendaciones) │
└──────────────────┘                                            └──────────────────────────┘
```

---

# 🧩 **3. Resumen ultra‑compacto de la arquitectura**

### **Componentes**
- **Backend API** (FastAPI)  
- **LangGraph** (control de flujo)  
- **Ollama** (LLMs locales)  
- **3 agentes**:
  - Planner Agent  
  - Search Agent  
  - Itinerary Builder  
- **RAG** (Chroma/Qdrant + embeddings)  
- **APIs externas** (vuelos, hoteles, tours, mapas)  
- **Docker** para despliegue  

### **Flujo**
1. Usuario → `/plan`  
2. Planner Agent → genera estructura del viaje  
3. `/search` → Search Agent → llama APIs externas  
4. `/itinerary` → Itinerary Builder → usa RAG + mapas  
5. Devuelve itinerario final optimizado  


# . ¿Cómo sería la experiencia del usuario?**

El usuario escribe:

> “Quiero viajar a Japón 10 días en octubre, saliendo desde Madrid. Me gustan los templos y la comida.”

El chatbot:

1. **Planner Agent** interpreta intención  
2. **Search Agent** busca vuelos, hoteles, tours  
3. **Itinerary Builder** usa RAG + mapas para crear un itinerario  
4. Devuelve una respuesta conversacional:

> “Perfecto, Pao. Te propongo este itinerario de 10 días en Japón…”

Todo fluye como un **chat natural**, pero con inteligencia real detrás.

---

# 🧩 **3. ¿Qué parte hace que sea un chatbot?**

### **A. El frontend (UI de chat)**
Puede ser:
- React  
- Next.js  
- Streamlit  
- Telegram bot  
- WhatsApp bot  
- Web simple con HTML/JS  

### **B. El backend**
Recibe mensajes del usuario y los envía a LangGraph.

### **C. LangGraph**
Decide qué agente debe responder.

### **D. Ollama**
Genera la respuesta en lenguaje natural.

---

# 🏗️ **4. Arquitectura conversacional (diagrama)**

```
Usuario (chat UI)
        │
        ▼
┌──────────────────────────┐
│      Backend API         │
│     (FastAPI/Flask)      │
└─────────────┬────────────┘
              │ mensaje del usuario
              ▼
┌──────────────────────────┐
│       LangGraph          │
│  (flujo conversacional)  │
└─────────────┬────────────┘
              │
   ┌──────────┼───────────┬───────────┐
   ▼          ▼           ▼            ▼
Planner   Search Agent   Itinerary   RAG
Agent     (APIs reales)   Builder   (contexto)
              │
              ▼
     APIs externas (vuelos, hoteles, tours, mapas)
              │
              ▼
Respuesta final en lenguaje natural
              │
              ▼
Usuario (chat)
```

---

# 🧩 **5. ¿Qué necesitas para que funcione como chatbot?**

### ✔ Un **frontend** que envíe mensajes al backend  
### ✔ Un **endpoint** `/chat` que reciba texto  
### ✔ LangGraph para decidir qué agente responde  
### ✔ Ollama para generar texto  
### ✔ RAG para dar contexto  
### ✔ APIs externas para datos reales  


