from dotenv import load_dotenv
load_dotenv()

from services.flights.flight_destination_service import FlightDestinationService


def test_search_destination():
    results = FlightDestinationService.search_destination("malaga")

    print("Resultados:", results)

    assert isinstance(results, list)
    assert len(results) > 0

    # Validación básica
    first = results[0]
    assert "name" in first
    assert "type" in first

    print("Primer resultado:", first)


if __name__ == "__main__":
    test_search_destination()
