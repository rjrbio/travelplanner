from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


class ItineraryAgent:
    """
    Agente encargado de construir el itinerario final de viaje utilizando IA.
    """

    def __init__(self):
        self.llm = ChatOllama(model="qwen3:8b", temperature=0.7)

    def build_itinerary(self, destination: str, days: int) -> dict:
        print(f"Creando itinerario de {days} días para {destination}...")

        with open("prompts/itinerary.txt", "r", encoding="utf-8") as file:
            prompt_text = file.read()

        prompt_template = ChatPromptTemplate.from_template(prompt_text)

        chain = prompt_template | self.llm

        response = chain.invoke({"destination": destination, "days": days})

        lineas = response.content.strip().split("\n")

        itinerario_limpio = [linea for linea in lineas if linea.strip() != ""]

        itinerario_exacto = itinerario_limpio[:days]

        while len(itinerario_exacto) < days:
            itinerario_exacto.append(
                f"Día {len(itinerario_exacto)+1}: Exploración libre en {destination}"
            )

        return {
            "destination": destination,
            "days": days,
            "itinerary": itinerario_exacto,
        }
