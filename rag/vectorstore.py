class VectorStore:
    def __init__(self) -> None:
        self.vectors: list[dict] = []

    def add(self, document_id: str, vector: list[float]) -> None:
        self.vectors.append({"id": document_id, "vector": vector})

    def search(self, query_vector: list[float], top_k: int = 5) -> list[dict]:
        return self.vectors[:top_k]
