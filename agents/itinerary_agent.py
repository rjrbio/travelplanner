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
    
    def itinerary_agent(state):
        """
        Agente final del grafo.
        Recibe:
            - flights
            - attractions
            - rag_data
            - plan
        Devuelve:
            - itinerario final en texto
        """

        itinerary = state.get("itinerary", {})

        summary = itinerary.get("summary", "Itinerario de viaje")
        days = itinerary.get("days", [])
        flights = itinerary.get("flights", [])
        attractions = itinerary.get("attractions", [])
        tips = itinerary.get("tips", [])
        weather = itinerary.get("weather")
        transport = itinerary.get("transport")
        events = itinerary.get("events", [])
        neighborhoods = itinerary.get("neighborhoods", [])

        text = f"🧳 **{summary}**\n\n"

        # Vuelos
        if flights:
            text += "✈️ **Vuelos sugeridos:**\n"
            for f in flights[:3]:
                text += f"- {f.get('airline', 'Aerolínea')} — {f.get('price')} {f.get('currency', '')}\n"
            text += "\n"

        # Atracciones
        if attractions:
            text += "🎟️ **Atracciones recomendadas:**\n"
            for a in attractions[:5]:
                text += f"- {a.get('name')} — {a.get('price')} {a.get('currency', '')}\n"
            text += "\n"

        # Días del itinerario
        text += "📅 **Plan día por día:**\n"
        for day in days:
            text += f"\n### {day['title']}\n"
            text += f"{day['description']}\n"
            if day.get("suggested_activities"):
                text += "\nActividades sugeridas:\n"
                for act in day["suggested_activities"]:
                    text += f"- {act.get('name')}\n"

        # RAG
        text += "\n\n🌤️ **Clima promedio:** " + (weather or "No disponible")
        text += "\n🚇 **Transporte recomendado:** " + (transport or "No disponible")

        if events:
            text += "\n🎉 **Eventos típicos:**\n"
            for e in events:
                text += f"- {e}\n"

        if neighborhoods:
            text += "\n🏘️ **Barrios recomendados:**\n"
            for n in neighborhoods:
                text += f"- {n}\n"

        if tips:
            text += "\n💡 **Tips útiles:**\n"
            for t in tips:
                text += f"- {t}\n"

        return {
            **state,
            "final_itinerary_text": text
        }

