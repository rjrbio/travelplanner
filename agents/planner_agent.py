from dataclasses import dataclass

@dataclass
class PlannerAgent:
    def plan_trip(self, destination: str, days: int) -> dict:
        return {
            "destination": destination,
            "days": days,
            "recommendations": [
                f"Explora {destination} durante {days} días",
                "Incluye actividad local y opciones de transporte"
            ]
        }
from services.locations.location_service import LocationService

def validate_location(self, location: str):
        """
        Usa la API para validar que la ciudad existe.
        """
        result = LocationService.get_location(location)

        if not result:
            return None

        # Solo aceptamos ciudades reales (locality)
        if "locality" not in result["types"]:
            return None

        return result
