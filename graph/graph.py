from langgraph.graph import StateGraph, START, END
from graph.state import TravelState

from agents.planner_agent import PlannerAgent
from agents.search_agent import SearchAgent
from agents.itinerary_agent import ItineraryAgent

planner = PlannerAgent()
searcher = SearchAgent()
Itinerary = ItineraryAgent()


def plan_node(state: TravelState):
    print("--- Entrando al Planner ---")
    destino = state["destination"]
    dias = state["days"]
    respuesta = planner.plan_trip(destino, dias)
    return {"planner_summary": respuesta["summary"]}


def search_node(state: TravelState):
    print("--- Entrando al Searcher ---")
    destino = state["destination"]
    opciones = searcher.search_options(destino)
    return {"search_options": opciones}


def itinerary_node(state: TravelState):
    print("--- Entrando al Itinerary Builder ---")
    destino = state["destination"]
    dias = state["days"]
    plan = Itinerary.build_itinerary(destino, dias)
    return {"itinerary_final": plan}


builder = StateGraph(TravelState)

builder.add_node("planner", plan_node)
builder.add_node("searcher", search_node)
builder.add_node("itinerary", itinerary_node)

builder.add_edge(START, "planner")
builder.add_edge("planner", "searcher")
builder.add_edge("searcher", "itinerary")
builder.add_edge("itinerary", END)

graph = builder.compile()


def ejecutar_viaje(destino: str, dias: int) -> dict:
    estado_inicial = {
        "destination": destino,
        "days": dias
    }
    resultado_final = graph.invoke(estado_inicial)
    return {
        "destino": destino,
        "dias": dias,
        "mensaje_motivacional": resultado_final.get("planner_summary"),
        "opciones_busqueda": resultado_final.get("search_options"),
        "itinerario": resultado_final.get("itinerary_final")
    }


if __name__ == "__main__":
    estado_inicial = {
        "destination": "Kioto", "days": 4
    }
    print("\n -- Arrancando el LangGraph... ---")
    resultado = graph.invoke(estado_inicial)

    print("\n--- EL PLANNER ---\n")
    print(resultado["planner_summary"])

    print("\n--- OPCIONES DEL SEARCHER ---")
    for opcion in resultado["search_options"]:
        print(f" - {opcion}")

    print("\n--- ITINERARIO FINAL ---")
    for dia in resultado["itinerary_final"]["itinerary"]:
        print(f" {dia}")
