from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class PlanResponse(BaseModel):
    destination: str
    duration_days: int
    summary: str

@router.get("/plan", response_model=PlanResponse)
async def create_plan(destination: str = "Paris", days: int = 5):
    return {
        "destination": destination,
        "duration_days": days,
        "summary": f"Plan para {destination} en {days} días."
    }
