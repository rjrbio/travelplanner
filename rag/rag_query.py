from pathlib import Path
from typing import List, Optional, Dict, Any

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "embeddings" / "vectorstore"

MODEL_NAME = "nomic-embed-text"


class RAGQuery:
    def __init__(self):
        # Embeddings con Ollama
        self.embeddings = OllamaEmbeddings(model=MODEL_NAME)

        # Cargar Chroma persistente
        self.db = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=self.embeddings
        )

    def search(
        self,
        query: str,
        k: int = 5,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Realiza una búsqueda semántica en el vectorstore.
        metadata_filter permite filtrar por ciudad, categoría, etc.
        """

        if metadata_filter:
            results = self.db.similarity_search(
                query=query,
                k=k,
                filter=metadata_filter
            )
        else:
            results = self.db.similarity_search(query=query, k=k)

        formatted = []
        for r in results:
            formatted.append({
                "content": r.page_content,
                "metadata": r.metadata
            })

        return formatted

# Prueba rápida
if __name__ == "__main__":
    rag = RAGQuery()

    query = "que visitar en andalucia?"
    print(f"\n🔎 Consulta: {query}")

    results = rag.search(
        query=query,
        k=3,
        metadata_filter={"ciudad": "andalucia"}
    )

    for i, r in enumerate(results, 1):
        print(f"\n--- Resultado {i} ---")
        print("Categoría:", r["metadata"].get("categoria"))
        print("Ciudad:", r["metadata"].get("ciudad"))
        print("Fuente:", r["metadata"].get("source"))
        print(r["content"][:300], "...")