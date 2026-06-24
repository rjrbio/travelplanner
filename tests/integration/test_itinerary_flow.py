from dotenv import load_dotenv
load_dotenv()

from nodes.fetch_flights_node import fetch_flights_node
from nodes.fetch_attractions_node import fetch_attractions_node
from nodes.enrich_itinerary_node import enrich_itinerary_node


def test_itinerary_flow():

    # 1. Estado inicial simulado del PlannerAgent
    state = {
        "origin": "malaga",
        "destination": "madrid",
        "destination_city": "madrid",
        "depart_date": "2026-07-10",
        "return_date": "2026-07-15",
        "adults": 1,
        "cabin_class": "ECONOMY",
        "currency": "EUR",
        "language": "en-us",
        "attractions_limit": 3,
        "plan": {
            "summary": "Viaje de prueba a Madrid",
            "days": [
                {"title": "Día 1", "description": "Explorar el centro"},
                {"title": "Día 2", "description": "Museos y cultura"}
            ]
        },
        "rag_data": {
            "tips": ["Compra entradas online"],
            "weather": "Soleado",
            "transport": "Metro y bus",
            "events": ["Festival local"],
            "neighborhoods": ["Centro", "Malasaña"]
        }
    }

    # 2. Ejecutar nodo de vuelos
    state = fetch_flights_node(state)
    assert "flights" in state
    assert isinstance(state["flights"], list)
    assert len(state["flights"]) > 0

    # 3. Ejecutar nodo de atracciones
    state = fetch_attractions_node(state)
    assert "attractions" in state
    assert isinstance(state["attractions"], list)
    assert len(state["attractions"]) > 0

    # 4. Ejecutar nodo de enriquecimiento
    state = enrich_itinerary_node(state)
    assert "itinerary" in state

    itinerary = state["itinerary"]

    # Validaciones del itinerario final
    assert "summary" in itinerary
    assert "days" in itinerary
    assert len(itinerary["days"]) == 2
    assert "flights" in itinerary
    assert len(itinerary["flights"]) > 0
    assert "attractions" in itinerary
    assert len(itinerary["attractions"]) > 0

    print("Itinerario final OK:", itinerary)
