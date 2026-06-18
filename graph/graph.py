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
