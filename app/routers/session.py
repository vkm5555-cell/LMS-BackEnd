# routers/organization.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import db as database
from app.models.session import SessionModel

router = APIRouter(prefix="/session", tags=["session"])

@router.get("/list/all", summary="Get all sessions for dropdown")
async def get_all_sessions_for_dropdown(
    db: Session = Depends(database.get_db)
):
    sessions = (
        db.query(SessionModel.id, SessionModel.session)
        .filter(SessionModel.status == "active", SessionModel.is_deleted == None)
        .order_by(SessionModel.session.asc())
        .all()
    )

    return {
        "success": True,
        "message": "All sessions fetched successfully",
        "data": [
            {"id": s.id, "session": s.session}
            for s in sessions
        ]
    }