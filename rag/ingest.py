import os
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


# === CONFIGURACIÓN ===
BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "documents"
CHROMA_DIR = BASE_DIR / "embeddings" / "vectorstore"

MODEL_NAME = "nomic-embed-text"

# Lista de ciudades y regiones detectables
CIUDADES = [
    "madrid", "barcelona", "sevilla", "valencia",
    "malaga", "granada", "cordoba", "andalucia"
]


def extract_metadata(path: Path):
    """
    Extrae metadatos basados en:
    - carpeta principal → categoria
    - nombre del archivo → ciudad
    """
    relative = path.relative_to(DOCS_DIR)
    categoria = relative.parts[0]  # carpeta principal

    filename = path.stem.lower()

    ciudad = next((c for c in CIUDADES if c in filename), None)

    return {
        "categoria": categoria,
        "ciudad": ciudad,
        "filename": filename,
        "source": str(relative)
    }


def load_documents():
    docs = []

    for root, _, files in os.walk(DOCS_DIR):
        for f in files:
            path = Path(root) / f

            # Detectar tipo de archivo
            if f.lower().endswith(".pdf"):
                loader = PyPDFLoader(str(path))
            elif f.lower().endswith(".txt") or f.lower().endswith(".md"):
                loader = TextLoader(str(path), encoding="utf-8")
            else:
                continue

            metadata = extract_metadata(path)
            loaded_docs = loader.load()

            # Añadir metadatos a cada documento
            for d in loaded_docs:
                d.metadata.update(metadata)

            docs.extend(loaded_docs)

    return docs


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    return splitter.split_documents(documents)


def build_vectorstore(chunks):
    embeddings = OllamaEmbeddings(model=MODEL_NAME)

    # IDs únicos por chunk
    ids = []
    for i, chunk in enumerate(chunks):
        filename = chunk.metadata.get("filename", "doc")
        ids.append(f"{filename}_{i}")

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        ids=ids,
        persist_directory=str(CHROMA_DIR),  # Persistencia automática
    )

    return vectordb


def main():
    print("📂 Cargando documentos...")
    documents = load_documents()
    print(f"   → {len(documents)} documentos cargados")

    print("✂️ Dividiendo en chunks...")
    chunks = split_documents(documents)
    print(f"   → {len(chunks)} chunks generados")

    print("🧠 Creando vectorstore con Chroma + Ollama...")
    vectordb = build_vectorstore(chunks)
    print(f"   → Vectorstore guardado en {CHROMA_DIR}")

    # Prueba rápida
    query = "mejores barrios para alojarse en Madrid"
    print(f"\n🔎 Prueba de búsqueda: {query}")
    results = vectordb.similarity_search(query, k=3)

    for r in results:
        print("\n--- Resultado ---")
        print("Categoría:", r.metadata.get("categoria"))
        print("Ciudad:", r.metadata.get("ciudad"))
        print("Fuente:", r.metadata.get("source"))
        print(r.page_content[:300], "...")


if __name__ == "__main__":
    main()
