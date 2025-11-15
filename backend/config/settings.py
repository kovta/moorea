"""Application configuration settings."""

import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # App settings
    app_name: str = "Moodboard Generator"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Database
    database_url: Optional[str] = None
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    
    # External APIs
    unsplash_access_key: Optional[str] = None
    pexels_api_key: Optional[str] = None
    flickr_api_key: Optional[str] = None
    
    # Pinterest API
    pinterest_access_token: Optional[str] = None
    
    # reCAPTCHA
    recaptcha_secret_key: Optional[str] = None
    
    # ML Model settings - Optimized for speed with more images
    clip_model_name: str = "RN50"  # Faster ResNet-50 model vs ViT-B/32
    clip_backend: str = "fashion"
    max_candidates: int = 20  # Reduced for faster processing
    final_moodboard_size: int = 12  # Reduced for faster generation
    
    # File paths - will be computed in __init__
    data_dir: Optional[Path] = None
    project_root: Optional[Path] = None
    cache_dir: Optional[Path] = None
    aesthetics_file: Optional[Path] = None
    
    def model_post_init(self, __context) -> None:
        """Compute file paths after model initialization."""
        import logging
        logger = logging.getLogger(__name__)
        
        # Find the data directory, checking backend/ first (Railway), then repo root (local dev)
        current_file = Path(__file__)  # config/settings.py
        backend_dir = current_file.parent.parent  # backend/
        repo_root = backend_dir.parent  # repo root
        
        logger.info(f"🔍 Looking for aesthetics.yaml file...")
        logger.info(f"   Current file: {current_file}")
        logger.info(f"   Backend dir: {backend_dir}")
        logger.info(f"   Repo root: {repo_root}")
        logger.info(f"   Checking backend/data/: {(backend_dir / 'data' / 'aesthetics.yaml').exists()}")
        logger.info(f"   Checking repo_root/data/: {(repo_root / 'data' / 'aesthetics.yaml').exists()}")
        
        # Check if data/ exists in backend directory (Railway structure - preferred)
        backend_data_path = backend_dir / "data" / "aesthetics.yaml"
        if backend_data_path.exists():
            self.data_dir = backend_dir / "data"
            logger.info(f"✅ Found aesthetics.yaml in backend/data/: {backend_data_path}")
        # Fallback: check if data/ exists in parent directory (repo root structure)
        elif (repo_root / "data" / "aesthetics.yaml").exists():
            self.data_dir = repo_root / "data"
            logger.info(f"✅ Found aesthetics.yaml in repo root/data/: {repo_root / 'data' / 'aesthetics.yaml'}")
        # Final fallback: use backend directory
        else:
            self.data_dir = backend_dir / "data"
            logger.warning(f"⚠️  aesthetics.yaml not found, using fallback path: {self.data_dir / 'aesthetics.yaml'}")
        
        self.project_root = self.data_dir.parent
        self.cache_dir = self.project_root / "cache"
        self.aesthetics_file = self.data_dir / "aesthetics.yaml"
        
        logger.info(f"📁 Final paths:")
        logger.info(f"   data_dir: {self.data_dir}")
        logger.info(f"   aesthetics_file: {self.aesthetics_file}")
        logger.info(f"   aesthetics_file exists: {self.aesthetics_file.exists()}")
    
    # Cache settings
    classification_cache_ttl: int = 86400 * 7  # 7 days
    api_cache_ttl: int = 86400  # 24 hours
    embedding_cache_ttl: int = 86400 * 30  # 30 days
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()