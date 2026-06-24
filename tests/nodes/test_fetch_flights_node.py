from dotenv import load_dotenv
load_dotenv()

from nodes.fetch_flights_node import fetch_flights_node


def test_fetch_flights_node():

    state = {
        "origin": "malaga",
        "destination": "madrid",
        "depart_date": "2026-07-10",
        "return_date": "2026-07-15",
        "adults": 1,
        "cabin_class": "ECONOMY",
        "currency": "EUR"
    }

    result = fetch_flights_node(state)

    assert "flights" in result
    assert isinstance(result["flights"], list)
    assert len(result["flights"]) > 0

    flight = result["flights"][0]
    assert "price" in flight
    assert "airline" in flight or "carrier" in flight
    assert "departure" in flight
    assert "arrival" in flight

    print("Vuelos OK:", result["flights"][:2])
