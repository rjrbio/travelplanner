import os
import requests

RAPIDAPI_HOST = "booking-com15.p.rapidapi.com"
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")


class SearchFlightsService:

    BASE_URL = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"

    @staticmethod
    def search_flights(
        from_id: str,
        to_id: str,
        depart_date: str,
        return_date: str = None,
        adults: int = 1,
        children: str = "0",
        stops: str = "none",
        page_no: int = 1,
        sort: str = "BEST",
        cabin_class: str = "ECONOMY",
        currency: str = "EUR"
    ):
        """
        Llama al endpoint Search Flights.
        Devuelve una lista normalizada de ofertas de vuelo.
        """

        headers = {
            "Content-Type": "application/json",
            "x-rapidapi-host": RAPIDAPI_HOST,
            "x-rapidapi-key": RAPIDAPI_KEY
        }

        params = {
            "fromId": from_id,
            "toId": to_id,
            "departDate": depart_date,
            "stops": stops,
            "pageNo": page_no,
            "adults": adults,
            "children": children,
            "sort": sort,
            "cabinClass": cabin_class,
            "currency_code": currency
        }

        # returnDate es opcional
        if return_date:
            params["returnDate"] = return_date

        response = requests.get(SearchFlightsService.BASE_URL, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f"Error en API: {response.status_code} - {response.text}")

        data = response.json()

        offers = data.get("data", {}).get("flightOffers", [])

        normalized = []

        for offer in offers:
            try:
                first_segment = offer["segments"][0]
                price = offer["priceBreakdown"]["total"]

                normalized.append({
                    "departure": first_segment["departureTime"],
                    "arrival": first_segment["arrivalTime"],
                    "from": first_segment["departureAirport"]["name"],
                    "to": first_segment["arrivalAirport"]["name"],
                    "airline": first_segment["legs"][0]["carriersData"][0]["name"],
                    "duration_seconds": first_segment["totalTime"],
                    "price": f"{price['units']} {price['currencyCode']}"
                })
            except Exception:
                continue

        return normalized
