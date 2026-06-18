from fastapi import FastAPI
from backend.api import plan, search, itinerary

app = FastAPI(title="Travel Planner")

app.include_router(plan.router, prefix="", tags=["plan"])
app.include_router(search.router, prefix="", tags=["search"])
app.include_router(itinerary.router, prefix="", tags=["itinerary"])

@app.get("/health")
async def health_check():
    return {"status": "ok"}
