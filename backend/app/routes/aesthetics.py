"""Aesthetics endpoints."""

import logging

from fastapi import APIRouter, HTTPException, status

from models import AestheticsListResponse
from services.aesthetic_service import aesthetic_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/aesthetics", response_model=AestheticsListResponse)
async def get_aesthetics():
    """Get available aesthetic categories."""
    try:
        aesthetics_data = await aesthetic_service.get_all_aesthetics()
        vocabulary = await aesthetic_service.get_vocabulary()
        
        return AestheticsListResponse(
            aesthetics=vocabulary,  # Return list of aesthetic names
            total_count=len(vocabulary),
            version="1.0.0"
        )
        
    except Exception as e:
        logger.error(f"Error getting aesthetics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error getting aesthetics"
        )