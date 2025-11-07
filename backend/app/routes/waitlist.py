"""Waitlist routes for pre-launch email collection."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from database import get_db, WaitlistUser

router = APIRouter(prefix="/api/v1/waitlist", tags=["waitlist"])


class WaitlistSubscribeRequest(BaseModel):
    """Request model for waitlist subscription."""
    email: EmailStr
    name: Optional[str] = None


class WaitlistSubscribeResponse(BaseModel):
    """Response model for waitlist subscription."""
    success: bool
    message: str
    email: str


@router.post("/subscribe", response_model=WaitlistSubscribeResponse)
async def subscribe_to_waitlist(
    request: WaitlistSubscribeRequest,
    db: Session = Depends(get_db)
):
    """Subscribe an email to the waitlist.
    
    Validates the email format and prevents duplicate signups.
    """
    # Check if email already exists
    existing = db.query(WaitlistUser).filter(WaitlistUser.email == request.email).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already on the waitlist!"
        )
    
    # Create new waitlist entry
    waitlist_user = WaitlistUser(
        email=request.email,
        name=request.name,
        notified=False
    )
    
    try:
        db.add(waitlist_user)
        db.commit()
        db.refresh(waitlist_user)
        
        return WaitlistSubscribeResponse(
            success=True,
            message="Successfully added to waitlist! We'll notify you when we launch.",
            email=request.email
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add email to waitlist: {str(e)}"
        )




