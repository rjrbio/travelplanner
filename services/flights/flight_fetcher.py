from services.flights.flight_destination_service import FlightDestinationService
from services.flights.search_flights_service import SearchFlightsService


class FlightFetcher:

    @staticmethod
    def get_flights(origin: str, destination: str, depart_date: str,
                    return_date: str = None, adults: int = 1,
                    cabin_class: str = "ECONOMY", currency: str = "EUR"):

        # 1. Buscar IDs de origen y destino
        origin_results = FlightDestinationService.search_destination(origin)
        destination_results = FlightDestinationService.search_destination(destination)

        if not origin_results or not destination_results:
            return []

        from_id = origin_results[0].get("id")
        to_id = destination_results[0].get("id")

        if not from_id or not to_id:
            return []

        # 2. Buscar vuelos reales
        flights = SearchFlightsService.search_flights(
            from_id=from_id,
            to_id=to_id,
            depart_date=depart_date,
            return_date=return_date,
            adults=adults,
            cabin_class=cabin_class,
            currency=currency
        )

        return flights
