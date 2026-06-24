import os
import requests

RAPIDAPI_HOST = "booking-com15.p.rapidapi.com"
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")


class LocationService:

    BASE_URL = "https://booking-com15.p.rapidapi.com/api/v1/meta/locationToLatLong"

    @staticmethod
    def get_location(query: str):
        """
        Llama al endpoint Location to Lat Long.
        Devuelve lat, lng, nombre y tipos.
        """

        headers = {
            "Content-Type": "application/json",
            "x-rapidapi-host": RAPIDAPI_HOST,
            "x-rapidapi-key": RAPIDAPI_KEY
        }

        params = {"query": query}

        response = requests.get(LocationService.BASE_URL, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f"Error en API: {response.status_code} - {response.text}")

        data = response.json()

        # Normalizamos el primer resultado
        if not data.get("data"):
            return None

        item = data["data"][0]

        return {
            "name": item.get("name"),
            "lat": item["geometry"]["location"]["lat"],
            "lng": item["geometry"]["location"]["lng"],
            "types": item.get("types", []),
            "address": item.get("formatted_address")
        }
