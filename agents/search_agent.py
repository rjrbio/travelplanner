from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


class SearchAgent:
    """
    Agente encargado de buscar opciones reales de vuelos, hoteles y actividades,
    utilizando Inteligencia Artificial.
    """

    def __init__(self):
        # Se inicializa el "cerebro" en el momento en que nace el agente
        self.llm = ChatOllama(model="qwen3:8b", temperature=0.7)

    def search_options(self, query: str) -> list[str]:
        print(f"Buscando opciones en internet para '{query}'...")

        # 1. Por rapidez, esta vez se pondrá el prompt directamente en el código
        prompt_text = """
        Eres un buscador experto. Inventa 3 opciones (un vuelo, un hotel, y un tour) para la búsqueda: {query}.
        Escribe cada opción en una nueva línea y no escribas introducciones, solo devuelve las opciones.
        """

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