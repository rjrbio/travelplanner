from rag.embeddings import embed_text
from rag.vectorstore import VectorStore


def test_embed_text():
    vector = embed_text("Prueba de texto")
    assert isinstance(vector, list)


def test_vector_store_add_search():
    store = VectorStore()
    store.add("doc1", [1.0, 2.0, 3.0])
    results = store.search([1.0, 2.0, 3.0])
    assert len(results) == 1
