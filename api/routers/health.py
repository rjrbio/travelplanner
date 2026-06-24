from fastapi import APIRouter
from sqlalchemy import text
from api.deps.database import SessionLocal

router = APIRouter()


@router.get("/")
def health():
    db_ok = False
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        db_ok = True
    except Exception:
        db_ok = False
    return {"status": "ok" if db_ok else "degraded", "database": "connected" if db_ok else "unavailable"}
