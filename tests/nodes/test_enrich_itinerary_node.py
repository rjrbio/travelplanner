from nodes.enrich_itinerary_node import enrich_itinerary_node


def test_enrich_itinerary_node():

    state = {
        "plan": {
            "summary": "Plan de viaje de prueba",
            "days": [
                {"title": "Día 1", "description": "Explorar la ciudad"},
                {"title": "Día 2", "description": "Visitar museos"}
            ]
        },
        "flights": [
            {"price": 120, "airline": "Iberia", "departure": "AGP", "arrival": "MAD"}
        ],
        "attractions": [
            {"name": "Tour nocturno", "photo": "url1"},
            {"name": "Comida callejera", "photo": "url2"},
            {"name": "Museo local", "photo": "url3"}
        ],
        "rag_data": {
            "tips": ["Lleva agua", "Compra tickets online"],
            "weather": "Soleado",
            "transport": "Metro y bus",
            "events": ["Festival local"],
            "neighborhoods": ["Centro histórico"]
        }
    }

    result = enrich_itinerary_node(state)

    assert "itinerary" in result
    itinerary = result["itinerary"]

    assert "summary" in itinerary
    assert "days" in itinerary
    assert len(itinerary["days"]) == 2

    day1 = itinerary["days"][0]
    assert "suggested_activities" in day1
    assert len(day1["suggested_activities"]) > 0

    assert "flights" in itinerary
    assert len(itinerary["flights"]) > 0

    print("Itinerario enriquecido OK:", itinerary)
