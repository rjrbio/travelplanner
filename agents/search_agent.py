from dataclasses import dataclass

@dataclass
class SearchAgent:
    """
    Agente encargado de buscar opciones reales de vuelos, hoteles y actividades.
    En esta versión de prueba (MVP), devuelve datos mock estaticos para no bloquear al backend.
    """
    def search_options(self, query: str) -> list[str]:
        print(f"Buscando opciones en internet para '{query}'...")

        # Simulamos una respuesta que parezca real, devolviendo una lista de texto
        return [
            f"Vuelo barato encontrado para {query} con escala en París.",
            f"Hotel céntrico disponible para las fechas de {query}",
            f"Tour recomendado: Caminata guiada por {query}."
        ]
