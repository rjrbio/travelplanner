from dataclasses import dataclass

@dataclass
class ItineraryAgent:
    def build_itinerary(self, destination: str, days: int) -> dict:
        return {
            "destination": destination,
            "days": days,
            "itinerary": [
                f"Día 1: Llegada a {destination}",
                f"Día {days}: Actividades finales y cierre"
            ]
        }
