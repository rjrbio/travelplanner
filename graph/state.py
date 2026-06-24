from typing import TypedDict, List

class TravelState(TypedDict):
    """ 
    Estos son los datos que los agentes se irán pasando.
    Cada agente tomará los datos que necesite, hará su trabajo, y devolverá la mochila un poco más llena.
    """
    # Entradas iniciales (dadas por el usuario)
    destination: str
    days: int

    # Salidas del PlannerAgent (texto motivacional)
    planner_summary: str

    # Salida del SearchAgent (listado de opciones)
    search_options: List[str]

    # Salida del ItineraryAgent (diccionario con el plan final)
    itinerary_final: dict

