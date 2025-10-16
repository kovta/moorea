"""Moodboard generation endpoints."""

import hashlib
import io
import logging
from typing import Optional
from uuid import UUID, uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status, Form
from PIL import Image

from models import (
    JobStatus,
    MoodboardRequest,
    MoodboardResponse,
    JobStatusResponse,
    MoodboardResult
)
from services.job_service import job_service
from services.moodboard_service import moodboard_service

logger = logging.getLogger(__name__)
router = APIRouter()


def _validate_image_file(file: UploadFile) -> None:
    """Validate uploaded image file."""
    # Check file type
    allowed_types = {"image/jpeg", "image/png", "image/jpg", "image/webp"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type: {file.content_type}. Please use JPEG, PNG, or WebP format."
        )
    
    # Check file size (max 10MB)
    if hasattr(file, 'size') and file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size too large. Maximum 10MB allowed."
        )


def _calculate_file_hash(file_content: bytes) -> str:
    """Calculate SHA256 hash of file content."""
    return hashlib.sha256(file_content).hexdigest()


@router.post("/moodboard/generate", response_model=MoodboardResponse)
async def generate_moodboard(
    file: UploadFile = File(...),
    pinterest_consent: bool = Form(False)
):
    """Generate moodboard from uploaded clothing image."""
    try:
        # Validate file
        _validate_image_file(file)
        
        # Read file content
        file_content = await file.read()
        file_hash = _calculate_file_hash(file_content)
        
        # Check if we already processed this image
        existing_job = await job_service.get_job_by_image_hash(file_hash)
        if existing_job:
            logger.info(f"Found existing job for image hash: {file_hash}")
            return MoodboardResponse(
                job_id=existing_job.id,
                status=existing_job.status,
                message="Using existing processing result for this image"
            )
        
        # Validate image can be opened
        try:
            image = Image.open(io.BytesIO(file_content))
            image.verify()  # Verify it's a valid image
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid image file: {str(e)}"
            )
        
        # Create new job
        job_id = uuid4()
        await job_service.create_job(
            job_id=job_id,
            image_hash=file_hash,
            image_content=file_content
        )
        
        # Queue moodboard generation
        await moodboard_service.queue_generation(job_id, file_content, pinterest_consent)
        
        logger.info(f"Queued moodboard generation job: {job_id}")
        
        return MoodboardResponse(
            job_id=job_id,
            status=JobStatus.PENDING,
            message="Moodboard generation started. Use job_id to check status."
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating moodboard: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during moodboard generation"
        )


@router.get("/moodboard/status/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: UUID):
    """Get job processing status."""
    try:
        job = await job_service.get_job_status(job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        return JobStatusResponse(
            job_id=job.id,
            status=job.status,
            progress=job.progress,
            created_at=job.created_at,
            completed_at=job.completed_at,
            error_message=job.error_message
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error getting job status"
        )


@router.get("/moodboard/result/{job_id}", response_model=MoodboardResult)
async def get_moodboard_result(job_id: UUID):
    """Get completed moodboard result."""
    try:
        result = await job_service.get_job_result(job_id)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job result not found"
            )
        
        if result.status != JobStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Job not completed. Current status: {result.status}"
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting moodboard result: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error getting moodboard result"
        )