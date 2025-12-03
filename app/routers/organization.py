# routers/organization.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import db as database
from app.models.organization import Organization

router = APIRouter(prefix="/organizations", tags=["Organizations"])

@router.get("/list/all", summary="Get all organizations for dropdown")
async def get_all_organizations_for_dropdown(
    db: Session = Depends(database.get_db)
):
    organizations = (
        db.query(Organization.id, Organization.org_name)
        .filter(Organization.org_status == "active", Organization.is_deleted == None)
        .order_by(Organization.org_name.asc())
        .all()
    )

    return {
        "success": True,
        "message": "All organizations fetched successfully",
        "data": [
            {"id": org.id, "org_name": org.org_name}
            for org in organizations
        ]
    }