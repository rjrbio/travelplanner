def enrich_itinerary_node(state):
    plan = state.get("plan", {})
    attractions = state.get("attractions", [])
    rag_data = state.get("rag_data", {})

    enriched = {
        "summary": plan.get("summary"),
        "days": [],
        "attractions": attractions,
        "flights": state.get("flights", []),
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
