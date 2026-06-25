from typing import TypedDict, List


class TravelState(TypedDict):
    destination: str
    destination_city: str
    days: int

    # RAG context (de RAGAgent)
    rag_data: dict

    # Plan del PlannerAgent
    planner_summary: str

    # Atracciones reales (de fetch_attractions_node via RapidAPI)
    attractions: List[dict]

    # Itinerario final enriquecido (de enrich_itinerary_node)
    itinerary: dict
