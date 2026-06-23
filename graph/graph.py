from langgraph.graph import StateGraph, START, END
from graph.state import TravelState

# Importamos los 3 agentes que hemos creado
from agents.planner_agent import PlannerAgent
from agents.search_agent import SearchAgent
from agents.itinerary_agent import ItineraryAgent

# 1. Instanciamos los agentes
planner=PlannerAgent()
searcher=SearchAgent()
Itinerary=ItineraryAgent()

# 2. Se crea el nodo 1: Planner
def plan_node(state: TravelState):
    print("--- Entrando al Planner ---")

    # El agente lee lo que hay en el state (destino y días)
    destino=state["destination"]
    dias=state["days"]

    # El agente empieza a trabajar
    respuesta=planner.plan_trip(destino, dias)

    # Devuelve solo la parte del state que hemos modificado
    return {"planner_summary":respuesta["summary"]}

# 3. Se crea el nodo 2: Searcher
def search_node(state:TravelState):
    print("--- Entrando al Searcher ---")
    destino=state["destination"]

    # El agente busca opciones (solo le pasamos el destino como query)
    opciones=searcher.search_options(destino)

    return {"search_options":opciones}

# 4. Se crea el nodo 3: Itinerary Builder
def itinerary_node(state:TravelState):
    print("--- Entrando al Itinerary Builder ---")
    destino=state["destination"]
    dias=state["days"]

    # El agente construye el plan final
    plan=Itinerary.build_itinerary(destino, dias)
    
    return {"itinerary_final":plan}

"""
5. Construimos los Graph
"""
builder=StateGraph(TravelState)

# Se añade los nodes
builder.add_node("planner", plan_node)
builder.add_node("searcher", search_node)
builder.add_node("itinerary", itinerary_node)

# Conectamos los nodes en el orden correcto
builder.add_edge(START, "planner")
builder.add_edge("planner", "searcher")
builder.add_edge("searcher", "itinerary")
builder.add_edge("itinerary", END)

# Por último, compilamos el graph para dejarla lista
graph=builder.compile()

if __name__=="__main__":
    # Crea el state inicial con lo que pide con lo que pide el usuario
    estado_inicial={
        "destination":"Kioto", "days":4
    }
    print("\n -- Arrancando el LangGraph... ---")
    
    # Invoca el graph pasándole el state inicial
    resultado=graph.invoke(estado_inicial)

    print ("\n--- EL PLANNER ---\n")
    print(resultado["planner_summary"])

    print("\n--- OPCIONES DEL SEARCHER ---")
    for opcion in resultado["search_options"]:
        print(f" - {opcion}")
        
    print("\n--- ITINERARIO FINAL ---")
    for dia in resultado["itinerary_final"]["itinerary"]:
        print(f" {dia}")



