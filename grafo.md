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
    - APIs de hoteles
    - APIs de clima
    - APIs de transporte
    - APIs de eventos
└─────────────┬────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────┐
│               6. OUTPUT NODE             │
│------------------------------------------│
│ • Devuelve el itinerario final al usuario│
└──────────────────────────────────────────┘
