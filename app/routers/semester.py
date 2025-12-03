# routers/semester.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import db as database
from app.models.semester import Semester

router = APIRouter(prefix="/semesters", tags=["Semesters"])

@router.get("/list/all", summary="Get all semesters for dropdown")
async def get_all_semesters_for_dropdown(
    db: Session = Depends(database.get_db)
):
    semesters = (
        db.query(Semester.code, Semester.name)
        .order_by(Semester.name.asc())
        .all()
    )

    return {
        "success": True,
        "message": "All semesters fetched successfully",
        "data": [
            {"code": s.code, "name": s.name}
            for s in semesters
        ]
    }