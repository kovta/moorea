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
    pinterest_client_id: Optional[str] = None
    pinterest_client_secret: Optional[str] = None
    pinterest_redirect_uri: str = "http://localhost:3000/auth/pinterest/callback"
    
    # ML Model settings
    clip_model_name: str = "ViT-B/32"
    max_candidates: int = 50
    final_moodboard_size: int = 12
    
    # File paths
    project_root: Path = Path(__file__).parent.parent.parent
    data_dir: Path = project_root / "data"
    cache_dir: Path = project_root / "cache"
    aesthetics_file: Path = data_dir / "aesthetics.yaml"
    
    # Cache settings
    classification_cache_ttl: int = 86400 * 7  # 7 days
    api_cache_ttl: int = 86400  # 24 hours
    embedding_cache_ttl: int = 86400 * 30  # 30 days
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()