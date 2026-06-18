from pathlib import Path
from typing import list


def ingest_documents(source_path: str) -> list[dict]:
    source = Path(source_path)
    documents = []
    if not source.exists():
        return documents

    for path in source.rglob("*.txt"):
        documents.append({
            "path": str(path),
            "content": path.read_text(encoding="utf-8")
        })
    return documents
