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
