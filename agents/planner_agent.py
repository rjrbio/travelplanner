import os

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")


class PlannerAgent:
    """
    Agente encargado de crear el plan inicial del viaje. En esta fase del (MVP),
    utilizando IA real.
    """

    def __init__(self):
        self._llm = None

    @property
    def llm(self):
        if self._llm is None:
            self._llm = ChatOllama(
                model="qwen3:1.7b", temperature=0.7, num_predict=1024,
                base_url=OLLAMA_URL, client_kwargs={"timeout": 60},
            )
        return self._llm

    def plan_trip(self, destination: str, days: int, context: str = "") -> dict:
        print(f"Pensando un viaje a {destination} de {days} días...")

        with open("prompts/planner.txt", "r", encoding="utf-8") as file:
            prompt_text = file.read()

        prompt_template = ChatPromptTemplate.from_template(prompt_text)

        chain = prompt_template | self.llm

        response = chain.invoke({
            "destination": destination,
            "duration_days": days,
            "context": context,
        })

        return {
            "destination": destination,
            "duration_days": days,
            "summary": response.content,
            "status": "success",
            "mock": False,
        }
