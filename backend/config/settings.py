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
    
    # ML Model settings - Optimized for speed with more images
    clip_model_name: str = "RN50"  # Faster ResNet-50 model vs ViT-B/32
    clip_backend: str = "fashion"
    max_candidates: int = 20  # Reduced for faster processing
    final_moodboard_size: int = 12  # Reduced for faster generation
    
    # File paths - computed dynamically to handle both local and Railway deployments
    @staticmethod
    def _get_data_dir() -> Path:
        """Find the data directory, checking backend/ first (Railway), then repo root (local dev)."""
        current_file = Path(__file__)  # config/settings.py
        backend_dir = current_file.parent.parent  # backend/
        repo_root = backend_dir.parent  # repo root
        
        # Check if data/ exists in backend directory (Railway structure - preferred)
        if (backend_dir / "data" / "aesthetics.yaml").exists():
            return backend_dir / "data"
        # Fallback: check if data/ exists in parent directory (repo root structure)
        elif (repo_root / "data" / "aesthetics.yaml").exists():
            return repo_root / "data"
        # Final fallback: use backend directory (will create if needed)
        else:
            return backend_dir / "data"
    
    @property
    def data_dir(self) -> Path:
        """Get the data directory path."""
        return self._get_data_dir()
    
    @property
    def project_root(self) -> Path:
        """Get the project root directory."""
        return self.data_dir.parent
    
    @property
    def cache_dir(self) -> Path:
        """Get the cache directory path."""
        return self.project_root / "cache"
    
    @property
    def aesthetics_file(self) -> Path:
        """Get the aesthetics YAML file path."""
        return self.data_dir / "aesthetics.yaml"
    
    # Cache settings
    classification_cache_ttl: int = 86400 * 7  # 7 days
    api_cache_ttl: int = 86400  # 24 hours
    embedding_cache_ttl: int = 86400 * 30  # 30 days
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()