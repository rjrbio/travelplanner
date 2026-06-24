from langgraph.graph import StateGraph, START, END
from graph.state import TravelState


def _get_agents():
    from agents.planner_agent import PlannerAgent
    from agents.rag_agent import RAGAgent
    return PlannerAgent(), RAGAgent().run


def _get_nodes():
    from nodes.fetch_attractions_node import fetch_attractions_node
    from nodes.enrich_itinerary_node import enrich_itinerary_node
    return fetch_attractions_node, enrich_itinerary_node


def _synthesize_rag_context(rag_data: dict) -> str:
    parts = []
    if rag_data.get("weather"):
        parts.append(f"Clima: {rag_data['weather']}")
    if rag_data.get("transport"):
        parts.append(f"Transporte: {rag_data['transport']}")
    if rag_data.get("tips"):
        parts.append(f"Consejos: {'; '.join(rag_data['tips'][:3])}")
    if rag_data.get("events"):
        parts.append(f"Eventos: {'; '.join(rag_data['events'][:3])}")
    if rag_data.get("neighborhoods"):
        parts.append(f"Barrios: {'; '.join(rag_data['neighborhoods'][:3])}")
    return "\n".join(parts) if parts else "No hay información adicional disponible."


def _build_graph():
    planner, rag_runner = _get_agents()
    fetch_attractions, enrich_itinerary = _get_nodes()

    def rag_node(state: TravelState):
        print("--- Consultando RAG ---")
        destino = state["destination"]
        try:
            enriched = rag_runner({"destination_city": destino})
            return {"rag_data": enriched.get("rag_data", {})}
        except Exception:
            print("--- RAG no disponible, continuando sin contexto ---")
            return {"rag_data": {}}

    def plan_node(state: TravelState):
        print("--- Planificando viaje ---")
        destino = state["destination"]
        dias = state["days"]
        context = _synthesize_rag_context(state.get("rag_data", {}))
        respuesta = planner.plan_trip(destino, dias, context=context)
        return {"planner_summary": respuesta["summary"]}

    def attractions_node(state: TravelState):
        print("--- Buscando atracciones ---")
        destino = state["destination"]
        try:
            result = fetch_attractions({
                "destination_city": destino,
                "attractions_limit": 5,
            })
            return {"attractions": result.get("attractions", [])}
        except Exception:
            return {"attractions": []}

    def itinerary_node(state: TravelState):
        print("--- Ensamblando itinerario final ---")
        plan = {
            "summary": state.get("planner_summary", ""),
            "days": [],
        }
        try:
            result = enrich_itinerary({
                "plan": plan,
                "flights": [],
                "attractions": state.get("attractions", []),
                "rag_data": state.get("rag_data", {}),
            })
            return {"itinerary": result.get("itinerary", {})}
        except Exception:
            return {"itinerary": {"summary": plan["summary"], "days": [], "flights": [], "attractions": []}}

    builder = StateGraph(TravelState)
    builder.add_node("rag", rag_node)
    builder.add_node("planner", plan_node)
    builder.add_node("attractions", attractions_node)
    builder.add_node("itinerary", itinerary_node)

    builder.add_edge(START, "rag")
    builder.add_edge("rag", "planner")
    builder.add_edge("planner", "attractions")
    builder.add_edge("attractions", "itinerary")
    builder.add_edge("itinerary", END)

    return builder.compile()


_graph = None


def _get_graph():
    global _graph
    if _graph is None:
        _graph = _build_graph()
    return _graph


def ejecutar_viaje(destino: str, dias: int) -> dict:
    try:
        graph = _get_graph()
        estado_inicial = {"destination": destino, "days": dias}
        resultado_final = graph.invoke(estado_inicial)
        return {
            "destino": destino,
            "dias": dias,
            "mensaje_motivacional": resultado_final.get("planner_summary"),
            "opciones_busqueda": resultado_final.get("attractions", []),
            "itinerario": resultado_final.get("itinerary", {}),
        }
    except Exception:
        return {
            "destino": destino,
            "dias": dias,
            "mensaje_motivacional": f"Plan de {dias} días en {destino}.",
            "opciones_busqueda": [
                f"Vuelo a {destino} desde €150",
                f"Hotel en {destino} desde €60/noche",
                f"Tour guiado por {destino} €40",
            ],
            "itinerario": {
                "summary": f"Plan de {dias} días en {destino}",
                "days": [
                    {"title": f"Día {i+1}", "description": f"Exploración en {destino}", "suggested_activities": []}
                    for i in range(dias)
                ],
            },
        }


if __name__ == "__main__":
    resultado = ejecutar_viaje("Kioto", 4)
    print("\n--- PLAN ---\n")
    print(resultado["mensaje_motivacional"])
    print("\n--- ATRACCIONES ---")
    for a in resultado["opciones_busqueda"]:
        print(f" - {a}")
    print("\n--- ITINERARIO ---")
    it = resultado["itinerario"]
    for dia in it.get("days", []):
        print(f" {dia}")
