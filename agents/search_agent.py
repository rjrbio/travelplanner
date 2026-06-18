from dataclasses import dataclass

@dataclass
class SearchAgent:
    def search_options(self, query: str) -> dict:
        return {
            "query": query,
            "options": [
                f"Hotel recomendado para {query}",
                f"Tour destacado para {query}"
            ]
        }
