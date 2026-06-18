from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class SearchResponse(BaseModel):
    query: str
    results: list[str]

@router.get("/search", response_model=SearchResponse)
async def search_destinations(query: str = "Europa"):
    return {
        "query": query,
        "results": [
            f"Búsqueda de {query} - opción 1",
            f"Búsqueda de {query} - opción 2"
        ]
    }
