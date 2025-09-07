"""Main FastAPI application."""

import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from models import HealthResponse
from services.aesthetic_service import aesthetic_service
from services.clip_service import clip_service
from services.cache_service import cache_service
from app.routes import moodboard, aesthetics


# Configure logging to both console and file
import os
log_file = os.path.join(os.path.dirname(__file__), "..", "moodboard_backend.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler(log_file, mode='a')  # File output (append)
    ]
)
logger = logging.getLogger(__name__)
logger.info(f"🚀 Logging to file: {os.path.abspath(log_file)}")
logger.info("=" * 80)
logger.info("🌸 NEW BACKEND SESSION STARTED 🌸")
logger.info("=" * 80)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    logger.info("Starting up Moodboard Generator API...")
    
    # Initialize services
    await cache_service.initialize()
    await aesthetic_service.initialize()
    await clip_service.initialize()
    logger.info("Services initialized successfully")
    
    yield
    
    logger.info("Shutting down...")
    # Cleanup code here if needed


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered moodboard generation from clothing images",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(moodboard.router, prefix="/api/v1", tags=["moodboard"])
app.include_router(aesthetics.router, prefix="/api/v1", tags=["aesthetics"])


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version=settings.app_version
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version=settings.app_version
    )


@app.post("/debug/clear-logs")
async def clear_logs():
    """Clear the log file for testing - DEBUG ONLY."""
    log_file = os.path.join(os.path.dirname(__file__), "..", "moodboard_backend.log")
    try:
        with open(log_file, 'w') as f:
            f.write("")
        logger.info("🧹 LOG FILE CLEARED FOR NEW TEST SESSION")
        return {"status": "logs_cleared", "message": "Log file cleared for new test session"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to clear logs: {str(e)}"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )