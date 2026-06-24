from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


class PlannerAgent:
    """
    Agente encargado de crear el plan inicial del viaje. En esta fase del (MVP),
    utilizando IA real.
    """

    def __init__(self):
        # Se inicializa el "cerebro" en el momento en que nace el agente
        self.llm = ChatOllama(model="qwen3:8b", temperature=0.7)

    def plan_trip(self, destination: str, days: int) -> dict:
        print(f"Pensando un viaje a {destination} de {days} días...")

        # 1. Se lee el archivo de instrucciones (prompt) que se creo en el Sprint 1
        with open("prompts/planner.txt", "r", encoding="utf-8") as file:
            prompt_text = file.read()

        # 2. Se crea la plantilla de langChain con el texto
        prompt_template = ChatPromptTemplate.from_template(prompt_text)

        # 3. Se une la plantilla con el modelo IA (Creamos la cadena / chain)
        chain = prompt_template | self.llm

        # 4. Se ejecuta la IA pasándole las variables (destino y días)
        response = chain.invoke({"destination": destination, "duration_days": days})

        # 5. Se devuelve el diccionario con la respuesta real de la IA
        return {
            "destination": destination,
            "duration_days": days,
            "summary": response.content,  # Aquí se guarda el texto gigante que inventó la IA
            "status": "success",
            "mock": False,  # No es un simulacro
        }
from services.locations.location_service import LocationService

def validate_location(self, location: str):
        """
        Usa la API para validar que la ciudad existe.
        """
        result = LocationService.get_location(location)

        if not result:
            return None

        # Solo aceptamos ciudades reales (locality)
        if "locality" not in result["types"]:
            return None

        return result
