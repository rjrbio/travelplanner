from dotenv import load_dotenv
load_dotenv()

from services.flights.flight_fetcher import FlightFetcher


def test_flight_fetcher():

    flights = FlightFetcher.get_flights(
        origin="malaga",
        destination="madrid",
        depart_date="2026-07-10",
        return_date="2026-07-15",
        adults=1,
        cabin_class="ECONOMY",
        currency="EUR"
    )

    print("Vuelos:", flights[:2])

    assert isinstance(flights, list)
    assert len(flights) > 0
    assert "price" in flights[0]


if __name__ == "__main__":
    test_flight_fetcher()
