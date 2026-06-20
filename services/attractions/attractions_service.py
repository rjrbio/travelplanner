import os
import requests

RAPIDAPI_HOST = "booking-com15.p.rapidapi.com"
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")


class AttractionsService:

    BASE_URL = "https://booking-com15.p.rapidapi.com/api/v1/attraction/searchAttractions"

    @staticmethod
    def search_attractions(encoded_id: str, page: int = 1, sort_by: str = "trending",
                           currency: str = "EUR", language: str = "en-us"):

        headers = {
            "Content-Type": "application/json",
            "x-rapidapi-host": RAPIDAPI_HOST,
            "x-rapidapi-key": RAPIDAPI_KEY
        }

        params = {
            "id": encoded_id,
            "sortBy": sort_by,
            "page": page,
            "currency_code": currency,
            "languagecode": language
        }

        response = requests.get(AttractionsService.BASE_URL, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f"Error en API: {response.status_code} - {response.text}")

        products = response.json().get("data", {}).get("products", [])

        normalized = []

        for p in products:
            normalized.append({
                "id": p.get("id"),
                "name": p.get("name"),
                "description": p.get("shortDescription"),
                "price": p.get("representativePrice", {}).get("chargeAmount"),
                "currency": p.get("representativePrice", {}).get("currency"),
                "rating": p.get("reviewsStats", {}).get("combinedNumericStats", {}).get("average"),
                "reviews": p.get("reviewsStats", {}).get("allReviewsCount"),
                "photo": p.get("primaryPhoto", {}).get("small"),
                "city": p.get("ufiDetails", {}).get("bCityName"),
                "country": p.get("ufiDetails", {}).get("url", {}).get("country")
            })

        return normalized
