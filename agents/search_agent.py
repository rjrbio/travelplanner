import os

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")


class SearchAgent:
    """
    Agente encargado de buscar opciones reales de vuelos, hoteles y actividades,
    utilizando Inteligencia Artificial.
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

    def search_options(self, query: str) -> list[str]:
        print(f"Buscando opciones en internet para '{query}'...")

        # 1. Leemos el archivo de instrucciones externas
        with open("prompts/search.txt", "r", encoding="utf-8") as file:
            prompt_text = file.read()

        # 2. Se crea la plantilla
        prompt_template = ChatPromptTemplate.from_template(prompt_text)

        # 3. Se ensambla el Pipe
        chain = prompt_template | self.llm

        # 4. Se invoca a la IA pasándole la búsqueda del usuario
        response = chain.invoke({"query": query})

        # 5. Se corta el texto gigante por saltos de línea (\n) para convertirlo en una lista
        opciones_separadas = response.content.strip().split("\n")

        # 6. Se limpia las líneas vacías por si la IA se pasó dejando espacios en blanco
        opciones_limpias = [
            opcion for opcion in opciones_separadas if opcion.strip() != ""
        ]

        return opciones_limpias