from dotenv import load_dotenv
load_dotenv()

from services.flights.flight_destination_service import FlightDestinationService
from services.flights.search_flights_service import SearchFlightsService


def test_search_flights_spain():

    # 1. Buscar IDs válidos
    origin = FlightDestinationService.search_destination("malaga")
    destination = FlightDestinationService.search_destination("madrid")

    assert len(origin) > 0
    assert len(destination) > 0

    from_id = origin[0]["id"]
    to_id = destination[0]["id"]

    print("FROM:", from_id)
    print("TO:", to_id)

    # 2. Buscar vuelos reales
    results = SearchFlightsService.search_flights(
        from_id=from_id,
        to_id=to_id,
        depart_date="2026-07-01",
        return_date="2026-07-05",
        adults=1,
        children="0",
        currency="EUR"
    )

    print("Resultados normalizados:", results[:3])

    assert isinstance(results, list)
    assert len(results) > 0


if __name__ == "__main__":
    test_search_flights_spain()
