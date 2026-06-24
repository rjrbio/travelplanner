import os
import requests

RAPIDAPI_HOST = "booking-com15.p.rapidapi.com"
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")


class FlightDestinationService:

    BASE_URL = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchDestination"

    @staticmethod
    def search_destination(query: str):
        """
        Llama al endpoint Search Flight Destination.
        Devuelve aeropuertos y ciudades relacionadas con el término.
        """

        headers = {
            "Content-Type": "application/json",
            "x-rapidapi-host": RAPIDAPI_HOST,
            "x-rapidapi-key": RAPIDAPI_KEY
        }

        params = {"query": query}

        response = requests.get(FlightDestinationService.BASE_URL, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f"Error en API: {response.status_code} - {response.text}")

        data = response.json()

        return data.get("data", [])
