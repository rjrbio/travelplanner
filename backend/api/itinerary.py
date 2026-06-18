from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ItineraryResponse(BaseModel):
    destination: str
    itinerary: list[str]

@router.get("/itinerary", response_model=ItineraryResponse)
async def get_itinerary(destination: str = "Roma"):
    return {
        "destination": destination,
        "itinerary": [
            "Día 1: Llegada y paseo por la ciudad",
            "Día 2: Visita a puntos principales",
            "Día 3: Actividad local"
        ]
    }
