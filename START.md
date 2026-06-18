**START — feature/rag-mock**

- **Propósito:** Poner en marcha la rama `feature/rag-mock` y dejar instrucciones para crear un RAG de prueba (mockable) sin dependencias externas (fallback en memoria).

- **Checklist rápida:**
  - `git pull origin feature/rag-mock`.
  - Entorno virtual: `python -m venv .venv` → `.\\.venv\\Scripts\\Activate.ps1`.
  - `pip install -r requirements.txt`.

- **Objetivos iniciales:**
  1. Adaptar `ej-chroma_persistente.py` para soportar un `VectorStore` en memoria y `embeddings` dummy cuando Chroma/Ollama no estén disponibles.
  2. Añadir un script `rag/mock_demo.py` con datos de ejemplo (txt/pdf) y un `README` corto sobre cómo ejecutar la demo.
  3. Añadir tests en `tests/test_rag.py` que validen el flujo mock (ingest → embed → search).

- **Comprobaciones locales:**
  - `python rag/mock_demo.py` → debe ejecutar sin Chroma y devolver resultados de búsqueda simulada.

- **Notas de colaboración:**
  - Documentar cambios en `ej-chroma_persistente.py` y dejar toggles para usar Chroma/Ollama o el fallback.
  - Mantener PRs pequeños y con ejemplos reproducibles.
