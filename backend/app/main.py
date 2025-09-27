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
from app.routes import moodboard, aesthetics, auth, moodboard_save
from database import create_tables


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    logger.info("Starting up Moodboard Generator API...")
    
    # Initialize database
    create_tables()
    logger.info("Database tables created")
    
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
app.include_router(auth.router, tags=["authentication"])
app.include_router(moodboard_save.router, tags=["moodboard-save"])


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


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )