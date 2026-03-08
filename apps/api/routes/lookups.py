from fastapi import APIRouter
from services.surreal import get_db

router = APIRouter(prefix="/lookups", tags=["lookups"])

@router.get("/bootstrap")
def get_bootstrap_data():
    db = get_db()

    areas = db.query("SELECT * FROM area ORDER BY name;")
    segments = db.query("SELECT * FROM segment ORDER BY name;")
    issues = db.query("SELECT * FROM issue ORDER BY name;")

    return {
        "areas": areas,
        "segments": segments,
        "issues": issues,
    }
