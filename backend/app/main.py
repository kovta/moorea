"""Main FastAPI application."""

import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from models import HealthResponse
from services.cache_service import cache_service
from app.routes import auth, pinterest_auth
from app.routes.waitlist import router as waitlist_router
from database import create_tables

# Optional routes that require ML dependencies
try:
    from app.routes import moodboard, aesthetics, moodboard_save
    MOODBOARD_ROUTES_AVAILABLE = True
except ImportError:
    moodboard = aesthetics = moodboard_save = None
    MOODBOARD_ROUTES_AVAILABLE = False

# Optional imports for ML features (gracefully handle if not installed)
try:
    from services.aesthetic_service import aesthetic_service
    from services.clip_service import clip_service
    ML_AVAILABLE = True
except ImportError:
    aesthetic_service = None
    clip_service = None
    ML_AVAILABLE = False


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    logger.info("Starting up Moodboard Generator API...")
    
    # Initialize database (optional, may fail locally without proper setup)
    try:
        create_tables()
        logger.info("Database tables created")
    except Exception as e:
        logger.warning(f"⚠️  Database initialization skipped: {str(e)}")
        logger.warning("✅ Pinterest OAuth endpoints will still work")
    
    # Initialize services (optional - gracefully handle failures)
    try:
        await cache_service.initialize()
        logger.info("Cache service initialized")
    except Exception as e:
        logger.warning(f"⚠️  Cache service initialization failed: {e}")
    
    if ML_AVAILABLE:
        try:
            await aesthetic_service.initialize()
            logger.info("Aesthetic service initialized")
        except Exception as e:
            logger.warning(f"Aesthetic service initialization failed (ML features disabled): {e}")
        
        try:
            await clip_service.initialize()
            logger.info("CLIP service initialized")
        except Exception as e:
            logger.warning(f"CLIP service initialization failed (ML features disabled): {e}")
    else:
        logger.warning("⚠️  ML libraries not installed - aesthetic/CLIP features disabled")
        logger.info("✅ Pinterest OAuth features are available")
    
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
import os
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "")

# Parse allowed origins from environment variable
# Format: "https://example.com,https://www.example.com,http://localhost:3000"
if allowed_origins_str:
    # Production: Use specific origins from environment variable
    allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]
    logger.info(f"CORS configured for production origins: {allowed_origins}")
else:
    # Development: Allow localhost and common dev origins
    allowed_origins = [
        "http://localhost:3000",  # React dev server
        "http://localhost:3001",  # Alternative React port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]
    logger.warning("⚠️  ALLOWED_ORIGINS not set - using development defaults. Set this in production!")

# CORS configuration
# Note: When allow_credentials=True, you CANNOT use allow_origins=["*"]
# Must specify exact origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,  # Required for cookies/auth tokens
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicit methods
    allow_headers=["*"],  # Allow all headers (Content-Type, Authorization, etc.)
    expose_headers=["*"],  # Expose all headers to frontend
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Include routers
if MOODBOARD_ROUTES_AVAILABLE:
    app.include_router(moodboard.router, prefix="/api/v1", tags=["moodboard"])
    app.include_router(aesthetics.router, prefix="/api/v1", tags=["aesthetics"])
    app.include_router(moodboard_save.router, tags=["moodboard-save"])
    logger.info("✅ Moodboard routes enabled")
else:
    logger.warning("⚠️  Moodboard routes disabled (ML dependencies not installed)")

app.include_router(auth.router, tags=["authentication"])
app.include_router(waitlist_router, tags=["waitlist"])
app.include_router(pinterest_auth.router, tags=["pinterest-oauth"])


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
    """Health check endpoint with database connectivity check."""
    from sqlalchemy import text
    from database import engine
    
    try:
        # Quick database connectivity check
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            conn.commit()
        
        return HealthResponse(
            status="healthy",
            timestamp=datetime.now(),
            version=settings.app_version
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        # Still return healthy to avoid false positives, but log the error
        # Railway will restart if the app actually crashes
        return HealthResponse(
            status="degraded",
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
