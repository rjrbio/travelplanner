from .state import GraphState

class LangGraph:
    def __init__(self) -> None:
        self.state = GraphState()
        self.nodes: dict[str, list[str]] = {
            "start": ["planner", "search"],
            "planner": ["itinerary"],
            "search": ["planner"],
            "itinerary": []
        }

    def transition(self, next_node: str) -> str:
        if next_node not in self.nodes:
            raise ValueError(f"Nodo inválido: {next_node}")
        self.state.current_node = next_node
        self.state.history.append(next_node)
        return next_node
    from langgraph.graph import StateGraph, END



    def build_graph():

        graph = StateGraph()

        # Nodos-agentes
        graph.add_node("classifier", classifier_agent)
        graph.add_node("rag", rag_agent)
        graph.add_node("budget", budget_agent)
        graph.add_node("planner", planner_agent)
        graph.add_node("itinerary", itinerary_agent)

        # Nodos de integración (Dev 3)
        graph.add_node("fetch_flights", fetch_flights_node)
        graph.add_node("fetch_attractions", fetch_attractions_node)
        graph.add_node("enrich_itinerary", enrich_itinerary_node)

        # Flujo del grafo
        graph.set_entry_point("classifier")

        graph.add_edge("classifier", "rag")
        graph.add_edge("rag", "budget")
        graph.add_edge("budget", "planner")

        # Integración Dev 3
        graph.add_edge("planner", "fetch_flights")
        graph.add_edge("fetch_flights", "fetch_attractions")
        graph.add_edge("fetch_attractions", "enrich_itinerary")
        graph.add_edge("enrich_itinerary", "itinerary")

        graph.add_edge("itinerary", END)

        return graph.compile()
