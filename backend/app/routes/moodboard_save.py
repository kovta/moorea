"""Moodboard routes for saving and managing user moodboards."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from database import get_db, User, Moodboard
from app.routes.auth import get_current_user

router = APIRouter(prefix="/api/v1/moodboards", tags=["moodboards"])

# Pydantic models
class MoodboardCreate(BaseModel):
    title: str
    description: Optional[str] = None
    aesthetic: str
    images: List[dict]  # List of image objects with URL, source, etc.

class MoodboardResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    aesthetic: str
    images: List[dict]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class MoodboardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

@router.post("/", response_model=MoodboardResponse)
async def create_moodboard(
    moodboard_data: MoodboardCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new moodboard for the current user."""
    db_moodboard = Moodboard(
        title=moodboard_data.title,
        description=moodboard_data.description,
        aesthetic=moodboard_data.aesthetic,
        images=moodboard_data.images,
        user_id=current_user.id
    )
    db.add(db_moodboard)
    db.commit()
    db.refresh(db_moodboard)
    return db_moodboard

@router.get("/", response_model=List[MoodboardResponse])
async def get_user_moodboards(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all moodboards for the current user."""
    moodboards = db.query(Moodboard).filter(Moodboard.user_id == current_user.id).all()
    return moodboards

@router.get("/{moodboard_id}", response_model=MoodboardResponse)
async def get_moodboard(
    moodboard_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific moodboard by ID."""
    moodboard = db.query(Moodboard).filter(
        Moodboard.id == moodboard_id,
        Moodboard.user_id == current_user.id
    ).first()
    
    if not moodboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Moodboard not found"
        )
    
    return moodboard

@router.put("/{moodboard_id}", response_model=MoodboardResponse)
async def update_moodboard(
    moodboard_id: int,
    moodboard_update: MoodboardUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a moodboard."""
    moodboard = db.query(Moodboard).filter(
        Moodboard.id == moodboard_id,
        Moodboard.user_id == current_user.id
    ).first()
    
    if not moodboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Moodboard not found"
        )
    
    # Update fields
    if moodboard_update.title is not None:
        moodboard.title = moodboard_update.title
    if moodboard_update.description is not None:
        moodboard.description = moodboard_update.description
    
    moodboard.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(moodboard)
    return moodboard

@router.delete("/{moodboard_id}")
async def delete_moodboard(
    moodboard_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a moodboard."""
    moodboard = db.query(Moodboard).filter(
        Moodboard.id == moodboard_id,
        Moodboard.user_id == current_user.id
    ).first()
    
    if not moodboard:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Moodboard not found"
        )
    
    db.delete(moodboard)
    db.commit()
    return {"message": "Moodboard deleted successfully"}
