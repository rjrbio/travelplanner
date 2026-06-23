def enrich_itinerary_node(state):
    """
    Node del grafo:
    - Combina el plan del PlannerAgent
    - Inserta vuelos
    - Inserta atracciones
    - Inserta datos del RAG
    - Devuelve el itinerario final enriquecido
    """

    plan = state.get("plan", {})
    flights = state.get("flights", [])
    attractions = state.get("attractions", [])
    rag_data = state.get("rag_data", {})

    enriched = {
        "summary": plan.get("summary"),
        "days": [],
        "flights": flights,
        "attractions": attractions,
        "tips": rag_data.get("tips"),
        "weather": rag_data.get("weather"),
        "transport": rag_data.get("transport"),
        "events": rag_data.get("events"),
        "neighborhoods": rag_data.get("neighborhoods")
    }

    # Enriquecer cada día del plan
    for day in plan.get("days", []):
        enriched_day = {
            "title": day.get("title"),
            "description": day.get("description"),
            "suggested_activities": attractions[:3],  # top 3 por día
            "weather": rag_data.get("weather"),
            "transport": rag_data.get("transport")
        }
        enriched["days"].append(enriched_day)

    return {
        **state,
        "itinerary": enriched
    }
