from fastapi import APIRouter

from services.surreal import get_db

router = APIRouter(prefix="/runs", tags=["runs"])


@router.get("/recent")
def get_recent_runs():
    db = get_db()
    runs = db.query("SELECT * FROM simulation_run ORDER BY created_at DESC LIMIT 10;")
    proposals = db.query("SELECT * FROM proposal ORDER BY id DESC LIMIT 10;")
    recommendations = db.query("SELECT * FROM recommendation ORDER BY id DESC LIMIT 10;")

    return {
        "runs": runs,
        "proposals": proposals,
        "recommendations": recommendations,
    }
