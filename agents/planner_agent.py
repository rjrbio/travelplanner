from dataclasses import dataclass

@dataclass
class PlannerAgent:
    """ 
    Agente encargado de crear el plan inicial del viaje. En esta fase del (MVP), 
    funciona como un 'mock' devolviendo datos estaticos
    """
    
    def plan_trip(self, destination: str, days: int) -> dict:
        print(f"Pensando un viaje a {destination} de {days} días...")
        # Devolvemos el JSON con la estructura que el backend espera.
        return {
            "destination": destination,
            "duration_days": days,
            # Cambiado para coincidir con el backend usamos summary en vez de recommendations
            "summary": f"Un viaje increíble de {days} días explorando lo mejor de {destination}.",
            "status": "success",
            "mock": True,
        }
