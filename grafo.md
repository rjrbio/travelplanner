┌──────────────────────────┐
│        USER QUERY        │
│  (texto libre del user)  │
└─────────────┬────────────┘
              │
              ▼
┌──────────────────────────────────────────┐
│        1. CLASSIFIER AGENT              │
│------------------------------------------│
│ • LLM rápido                             │
│ • Detecta intención                      │
│ • Detecta ciudades / regiones            │
│ • Detecta duración                       │
│ • Detecta presupuesto                    │
│ • Detecta categoría (gastronomía, etc.)  │
└─────────────┬────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────┐
│              2. RAG AGENT                │
│------------------------------------------│
│ • Tool: Chroma (vectorstore)             │
│ • Tool: OllamaEmbeddings                 │
│ • Recupera contexto relevante             │
│ • Filtra por ciudad / región / categoría │
└─────────────┬────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────┐
│             3. BUDGET AGENT              │
│------------------------------------------│
│ • Regex + LLM opcional                   │
│ • Normaliza presupuesto                  │
│   (low / medium / high / custom €) 
   APIs de conversión de moneda (opcional)      │
└─────────────┬────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────┐
│             4. PLANNER AGENT             │
│------------------------------------------│
│ • LLM                                     │
│ • Crea estructura del itinerario          │
│   - días                                  │
│   - ciudades                              │
│   - orden                                 │
│   - ritmo                                 │
│   - categorías por día                    │
│ • Ajusta según presupuesto                │
└─────────────┬────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────┐
│        5. ITINERARY BUILDER AGENT        │
│------------------------------------------│
│ • LLM                                     │
│ • Usa: plan + RAG context + presupuesto   │
│ • Genera el itinerario final              │
│   (texto completo, detallado y coherente)
    - APIs de vuelos
    - API de eventos
    - APIS de localizacion 
└─────────────┬────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────┐
│               6. OUTPUT NODE             │
│------------------------------------------│
│ • Devuelve el itinerario final al usuario│
└──────────────────────────────────────────┘


graph.add_node("classifier", classifier_node)   # LLM + regex + detectors
graph.add_node("rag", rag_node)                 # RAGQuery (Chroma + Embeddings)
graph.add_node("budget", budget_node)           # regex + (opcional LLM)
graph.add_node("planner", planner_node)         # PlannerAgent (LLM)
graph.add_node("itinerary", itinerary_node)     # ItineraryAgent (LLM + RAG)
graph.add_node("output", output_node)           # no tools