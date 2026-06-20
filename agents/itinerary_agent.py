from dataclasses import dataclass

from rag.rag_query import RAGQuery

@dataclass
class ItineraryAgent:
    def __init__(self):
        # Instanciamos el RAG una sola vez
        self.rag = RAGQuery()
    def build_itinerary(self, destination: str, days: int) -> dict:
        return {
            "destination": destination,
            "days": days,
            "itinerary": [
                f"Día 1: Llegada a {destination}",
                f"Día {days}: Actividades finales y cierre"
            ]
        }


    def get_rag_context(self, query: str, city: str = None, category: str = None, k: int = 5):
        """
        Llama al RAG para obtener contexto relevante.
        Este método es el que se usará desde el grafo.
        """

        metadata_filter = {}

        if city:
            metadata_filter["ciudad"] = city.lower()

        if category:
            metadata_filter["categoria"] = category.lower()

        # Llamada al RAG
        context = self.rag.search(
            query=query,
            k=k,
            metadata_filter=metadata_filter if metadata_filter else None
        )

        return context

    def build_itinerary_full(self, plan, rag_context, budget):
        """
        Genera el itinerario final combinando:
        - el plan del PlannerAgent
        - el contexto del RAG
        - el presupuesto normalizado
        """

        # Aquí luego integrarás vuelos, atracciones, etc.
        # Por ahora dejamos un esqueleto limpio.

        itinerary = {
            "summary": f"Itinerario generado para {plan.get('city')} con presupuesto {budget}",
            "days": []
        }

        for day in plan.get("days", []):
            day_info = {
                "day": day["day"],
                "city": day["city"],
                "activities": [],
                "rag_context_used": rag_context[:2]  # ejemplo: usamos los 2 primeros chunks
            }

            itinerary["days"].append(day_info)

        return itinerary
