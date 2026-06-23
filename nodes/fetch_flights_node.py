from services.flights.flight_fetcher import FlightFetcher

def fetch_flights_node(state):
    """
    Node del grafo:
    - Recibe origen, destino y fechas desde el PlannerAgent
    - Llama a FlightFetcher
    - Devuelve vuelos normalizados
    """

    origin = state.get("origin")
    destination = state.get("destination")
    depart_date = state.get("depart_date")
    return_date = state.get("return_date")
    adults = state.get("adults", 1)
    cabin_class = state.get("cabin_class", "ECONOMY")
    currency = state.get("currency", "EUR")

    flights = FlightFetcher.get_flights(
        origin=origin,
        destination=destination,
        depart_date=depart_date,
        return_date=return_date,
        adults=adults,
        cabin_class=cabin_class,
        currency=currency
    )

    return {
        **state,
        "flights": flights
    }
