from dataclasses import dataclass, field

@dataclass
class GraphState:
    current_node: str = "start"
    history: list[str] = field(default_factory=lambda: ["start"])
