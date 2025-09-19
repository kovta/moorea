"""Pydantic models for API requests and responses."""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    """Job processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AestheticScore(BaseModel):
    """Aesthetic classification result."""
    name: str = Field(..., description="Aesthetic category name")
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    description: Optional[str] = Field(None, description="Human-readable description of the aesthetic")


class ImageCandidate(BaseModel):
    """Image candidate from external APIs."""
    id: str = Field(..., description="Unique image identifier")
    url: str = Field(..., description="Full resolution image URL")
    thumbnail_url: Optional[str] = Field(None, description="Thumbnail image URL")
    photographer: Optional[str] = Field(None, description="Photographer name for attribution")
    source_api: str = Field(..., description="Source API (unsplash, pexels, flickr)")
    similarity_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="CLIP similarity score")
    download_location: Optional[str] = Field(None, description="Unsplash download tracking URL")


class MoodboardResponse(BaseModel):
    """Response for moodboard generation request."""
    job_id: UUID = Field(..., description="Job identifier for tracking")
    status: JobStatus = Field(..., description="Current job status")
    message: str = Field(..., description="Human-readable status message")


class JobStatusResponse(BaseModel):
    """Response for job status query."""
    job_id: UUID = Field(..., description="Job identifier")
    status: JobStatus = Field(..., description="Current job status")
    progress: Optional[int] = Field(None, ge=0, le=100, description="Processing progress percentage")
    created_at: datetime = Field(..., description="Job creation timestamp")
    completed_at: Optional[datetime] = Field(None, description="Job completion timestamp")
    error_message: Optional[str] = Field(None, description="Error message if status is FAILED")


class MoodboardResult(BaseModel):
    """Complete moodboard generation result."""
    job_id: UUID = Field(..., description="Job identifier")
    status: JobStatus = Field(..., description="Job status (should be COMPLETED)")
    top_aesthetics: List[AestheticScore] = Field(..., description="Detected aesthetic classifications")
    images: List[ImageCandidate] = Field(..., description="Curated moodboard images")
    created_at: datetime = Field(..., description="Result creation timestamp")
    processing_time: Optional[float] = Field(None, description="Total processing time in seconds")


class MoodboardRequest(BaseModel):
    """Request model for moodboard generation (if needed for form data)."""
    pass  # File upload is handled by FastAPI's UploadFile


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(..., description="Service health status")
    timestamp: datetime = Field(..., description="Health check timestamp")
    version: str = Field(..., description="API version")


class AestheticsListResponse(BaseModel):
    """Response for aesthetics vocabulary list."""
    aesthetics: List[str] = Field(..., description="Available aesthetic categories")
    total_count: int = Field(..., description="Total number of available aesthetics")
    version: str = Field(..., description="Aesthetic vocabulary version")


# For the MVP fast track - focused on dominant aesthetic
class SimplifiedMoodboardResult(BaseModel):
    """Simplified moodboard result focusing on dominant aesthetic."""
    job_id: UUID = Field(..., description="Job identifier")
    status: JobStatus = Field(..., description="Job status")
    dominant_aesthetic: AestheticScore = Field(..., description="Primary detected aesthetic")
    aesthetic_confidence: float = Field(..., ge=0.0, le=1.0, description="Overall classification confidence")
    images: List[ImageCandidate] = Field(..., description="Curated moodboard images")
    created_at: datetime = Field(..., description="Result creation timestamp")
    processing_time: Optional[float] = Field(None, description="Total processing time in seconds")
    total_images_available: int = Field(..., description="Total images available for endless scroll")

