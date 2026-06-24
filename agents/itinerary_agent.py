from dataclasses import dataclass


class ItineraryAgent:
    """
    Agente final del grafo.
    Recibe el estado enriquecido y genera el itinerario final en texto.
    """

    def run(self, state):
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


# Instancia global para el grafo
itinerary_agent = ItineraryAgent().run
