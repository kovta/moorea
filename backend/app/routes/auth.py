"""Authentication routes for user registration and login."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any

from database import get_db, User, Moodboard
from services.auth_service import (
    authenticate_user, create_user, create_access_token, 
    verify_token, get_user_by_username, get_user_by_email,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from services.recaptcha_service import recaptcha_service
from fastapi import Request

router = APIRouter(prefix="/api/v1/auth", tags=["authentication"])

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    recaptcha_token: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    username = verify_token(token)
    if username is None:
        raise credentials_exception
    
    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, request: Request, db: Session = Depends(get_db)):
    """Register a new user."""
    # Verify reCAPTCHA token
    if user_data.recaptcha_token:
        client_ip = request.client.host if request.client else None
        is_valid = await recaptcha_service.verify_token(user_data.recaptcha_token, client_ip)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="reCAPTCHA verification failed. Please try again."
            )
    else:
        # If reCAPTCHA is configured but token is missing, reject
        from config import settings
        if settings.recaptcha_secret_key:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="reCAPTCHA verification required"
            )
    
    # Check if username already exists
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = create_user(db, user_data.username, user_data.email, user_data.password)
    return user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    request: Request = None,
    db: Session = Depends(get_db)
):
    """Login user and return access token."""
    # Get reCAPTCHA token from request form data
    recaptcha_token = None
    if request:
        try:
            form_body = await request.form()
            recaptcha_token = form_body.get("recaptcha_token")
        except Exception:
            pass
    
    # Verify reCAPTCHA token if provided
    if recaptcha_token:
        client_ip = request.client.host if request and request.client else None
        is_valid = await recaptcha_service.verify_token(recaptcha_token, client_ip)
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="reCAPTCHA verification failed. Please try again."
            )
    else:
        # If reCAPTCHA is configured but token is missing, reject
        from config import settings
        if settings.recaptcha_secret_key:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="reCAPTCHA verification required"
            )
    
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user

@router.get("/export-data")
async def export_user_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> JSONResponse:
    """Export all user data for GDPR compliance.
    
    Returns a complete JSON export of all user data including:
    - Account information
    - All saved moodboards with full details
    - Metadata about data collection and usage
    
    This endpoint satisfies GDPR Article 20 (Right to Data Portability)
    and CCPA Section 1798.110 (Right to Know).
    """
    # Get all user moodboards
    moodboards = db.query(Moodboard).filter(Moodboard.user_id == current_user.id).all()
    
    # Prepare moodboard data
    moodboards_data = []
    for mb in moodboards:
        moodboards_data.append({
            "id": mb.id,
            "title": mb.title,
            "description": mb.description,
            "aesthetic": mb.aesthetic,
            "images": mb.images,  # JSON field with full image metadata
            "created_at": mb.created_at.isoformat() if mb.created_at else None,
            "updated_at": mb.updated_at.isoformat() if mb.updated_at else None
        })
    
    # Prepare complete export
    export_data = {
        "export_metadata": {
            "export_date": datetime.utcnow().isoformat(),
            "export_version": "1.0",
            "data_controller": "Moorea",
            "privacy_policy": "Moorea.mood.com/privacy",
            "contact_email": "annaszilviakennedy@gmail.com"
        },
        "user_account": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "is_active": current_user.is_active,
            "account_created": current_user.created_at.isoformat() if current_user.created_at else None,
            "last_updated": current_user.updated_at.isoformat() if current_user.updated_at else None
        },
        "moodboards": moodboards_data,
        "data_usage_summary": {
            "total_moodboards": len(moodboards_data),
            "data_stored": [
                "Account credentials (username, email, hashed password)",
                "Saved moodboards (titles, descriptions, image references)",
                "Session tokens (temporary, expire after 30 minutes)"
            ],
            "data_not_stored": [
                "Uploaded images (processed temporarily, not saved)",
                "Browsing history",
                "IP addresses",
                "Device information"
            ],
            "third_party_services": [
                "Unsplash (image source)",
                "Pexels (image source)",
                "Flickr (image source)",
                "Pinterest (image source, if enabled)"
            ]
        },
        "your_rights": {
            "right_to_access": "You are currently exercising this right",
            "right_to_rectification": "Update your data via account settings",
            "right_to_erasure": "Delete your account to remove all data",
            "right_to_data_portability": "This JSON export provides all your data",
            "right_to_object": "Contact us at annaszilviakennedy@gmail.com",
            "right_to_withdraw_consent": "Delete your account at any time"
        }
    }
    
    # Return as downloadable JSON
    return JSONResponse(
        content=export_data,
        headers={
            "Content-Disposition": f"attachment; filename=moorea_data_export_{current_user.username}_{datetime.utcnow().strftime('%Y%m%d')}.json",
            "Content-Type": "application/json"
        }
    )

@router.delete("/delete-account")
async def delete_user_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete user account and all associated data (GDPR Right to Erasure).
    
    This permanently deletes:
    - User account
    - All saved moodboards
    - All associated data
    
    This action cannot be undone.
    """
    # Delete all user's moodboards first (cascade should handle this, but being explicit)
    db.query(Moodboard).filter(Moodboard.user_id == current_user.id).delete()
    
    # Delete user account
    db.delete(current_user)
    db.commit()
    
    return {
        "message": "Account deleted successfully",
        "deleted_at": datetime.utcnow().isoformat(),
        "username": current_user.username
    }
