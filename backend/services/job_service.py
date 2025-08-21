"""Job management service for async processing."""

import logging
from datetime import datetime
from typing import Dict, Optional
from uuid import UUID

from models import JobStatus, MoodboardResult

logger = logging.getLogger(__name__)


class Job:
    """Simple job model for in-memory storage."""
    
    def __init__(self, job_id: UUID, image_hash: str):
        self.id = job_id
        self.image_hash = image_hash
        self.status = JobStatus.PENDING
        self.progress: Optional[int] = None
        self.created_at = datetime.now()
        self.completed_at: Optional[datetime] = None
        self.error_message: Optional[str] = None
        self.result: Optional[MoodboardResult] = None


class JobService:
    """Service for managing moodboard generation jobs."""
    
    def __init__(self):
        # In-memory job storage (use Redis/DB in production)
        self._jobs: Dict[UUID, Job] = {}
        self._hash_to_job: Dict[str, UUID] = {}
    
    async def create_job(self, job_id: UUID, image_hash: str, image_content: bytes) -> Job:
        """Create a new job."""
        job = Job(job_id, image_hash)
        self._jobs[job_id] = job
        self._hash_to_job[image_hash] = job_id
        
        logger.info(f"Created job {job_id} for image hash {image_hash[:8]}...")
        return job
    
    async def get_job_by_image_hash(self, image_hash: str) -> Optional[Job]:
        """Get existing job by image hash."""
        job_id = self._hash_to_job.get(image_hash)
        if job_id:
            return self._jobs.get(job_id)
        return None
    
    async def get_job_status(self, job_id: UUID) -> Optional[Job]:
        """Get job status."""
        return self._jobs.get(job_id)
    
    async def get_job_result(self, job_id: UUID) -> Optional[MoodboardResult]:
        """Get job result if completed."""
        job = self._jobs.get(job_id)
        if job and job.status == JobStatus.COMPLETED:
            return job.result
        return None
    
    async def update_job_status(self, job_id: UUID, status: JobStatus, 
                              progress: Optional[int] = None,
                              error_message: Optional[str] = None) -> None:
        """Update job status."""
        job = self._jobs.get(job_id)
        if job:
            job.status = status
            if progress is not None:
                job.progress = progress
            if error_message:
                job.error_message = error_message
            if status in [JobStatus.COMPLETED, JobStatus.FAILED]:
                job.completed_at = datetime.now()
    
    async def store_job_result(self, job_id: UUID, result: MoodboardResult) -> None:
        """Store completed job result."""
        job = self._jobs.get(job_id)
        if job:
            job.result = result
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.now()


# Global service instance
job_service = JobService()