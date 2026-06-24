import os
import logging
from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    CSVLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "documents"
CHROMA_DIR = BASE_DIR / "embeddings" / "vectorstore"

MODEL_NAME = "nomic-embed-text"

CIUDADES = [
    "madrid", "barcelona", "sevilla", "valencia",
    "malaga", "granada", "cordoba", "andalucia",
    "bilbao", "palma", "alicante", "tenerife",
]

LOADER_MAP = {
    ".pdf": PyPDFLoader,
    ".txt": lambda p: TextLoader(str(p), encoding="utf-8"),
    ".md": lambda p: TextLoader(str(p), encoding="utf-8"),
    ".csv": lambda p: CSVLoader(str(p), encoding="utf-8"),
}


def extract_metadata(path: Path):
    relative = path.relative_to(DOCS_DIR)
    categoria = relative.parts[0] if len(relative.parts) > 1 else "general"
    filename = path.stem.lower()
    ciudad = next((c for c in CIUDADES if c in filename), None)
    # Try to infer city from parent folder as fallback
    if not ciudad and len(relative.parts) > 2:
        folder_lower = relative.parts[-2].lower()
        ciudad = next((c for c in CIUDADES if c in folder_lower), None)
    return {
        "categoria": categoria,
        "ciudad": ciudad,
        "filename": filename,
        "source": str(relative),
    }


def load_file(path: Path) -> list:
    ext = path.suffix.lower()
    loader_fn = LOADER_MAP.get(ext)
    if loader_fn is None:
        logger.warning("Formato no soportado: %s", ext)
        return []
    try:
        loader = loader_fn(str(path))
        docs = loader.load()
        metadata = extract_metadata(path)
        for d in docs:
            d.metadata.update(metadata)
        logger.info("Cargado %s (%d páginas/chunks)", path.name, len(docs))
        return docs
    except Exception:
        logger.exception("Error cargando %s", path)
        return []


def load_documents(docs_dir: Path | None = None):
    docs_dir = docs_dir or DOCS_DIR
    docs = []
    for root, _, files in os.walk(docs_dir):
        for f in files:
            path = Path(root) / f
            docs.extend(load_file(path))
    return docs


def split_documents(documents, chunk_size=500, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    return splitter.split_documents(documents)


def build_vectorstore(chunks, chroma_dir: Path | None = None):
    chroma_dir = chroma_dir or CHROMA_DIR
    embeddings = OllamaEmbeddings(
        model=MODEL_NAME,
        client_kwargs={"timeout": 120},
    )
    ids = []
    for i, chunk in enumerate(chunks):
        filename = chunk.metadata.get("filename", "doc")
        ids.append(f"{filename}_{i}")
    try:
        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            ids=ids,
            persist_directory=str(chroma_dir),
        )
        return vectordb
    except Exception:
        logger.exception("Error construyendo vectorstore")
        raise


def get_collection_stats(chroma_dir: Path | None = None) -> dict:
    chroma_dir = chroma_dir or CHROMA_DIR
    try:
        embeddings = OllamaEmbeddings(
            model=MODEL_NAME,
            client_kwargs={"timeout": 10},
        )
        db = Chroma(
            persist_directory=str(chroma_dir),
            embedding_function=embeddings,
        )
        collection = db.get()
        return {
            "total_chunks": len(collection.get("ids", [])),
            "documents": list(set(
                m.get("source", "unknown")
                for m in collection.get("metadatas", [])
                if m
            )),
        }
    except Exception:
        logger.exception("Error obteniendo estadísticas")
        return {"total_chunks": 0, "documents": []}


def index_all(docs_dir: Path | None = None, chroma_dir: Path | None = None):
    logger.info("=== INICIO DE INDEXACIÓN ===")
    documents = load_documents(docs_dir)
    logger.info("Documentos cargados: %d", len(documents))
    if not documents:
        logger.warning("No hay documentos que indexar")
        return {"status": "empty", "documents": 0, "chunks": 0}
    chunks = split_documents(documents)
    logger.info("Chunks generados: %d", len(chunks))
    build_vectorstore(chunks, chroma_dir)
    logger.info("=== INDEXACIÓN COMPLETA ===")
    return {"status": "ok", "documents": len(documents), "chunks": len(chunks)}


def list_documents(docs_dir: Path | None = None) -> list[dict]:
    docs_dir = docs_dir or DOCS_DIR
    result = []
    for root, _, files in os.walk(docs_dir):
        category = Path(root).relative_to(docs_dir).parts[0] if root != str(docs_dir) else "general"
        for f in files:
            path = Path(root) / f
            ext = path.suffix.lower()
            if ext not in LOADER_MAP:
                continue
            metadata = extract_metadata(path)
            result.append({
                "name": f,
                "path": str(path.relative_to(docs_dir)),
                "category": metadata["categoria"],
                "city": metadata["ciudad"],
                "size": path.stat().st_size,
            })
    return result


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = index_all()
    print(f"\nResultado: {result}")
    stats = get_collection_stats()
    print(f"Stats: {stats}")
