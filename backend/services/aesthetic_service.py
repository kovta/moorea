"""Aesthetic classification and management service."""

import logging
from typing import Dict, List, Optional
import yaml

from config import settings

logger = logging.getLogger(__name__)


class AestheticService:
    """Service for managing aesthetic vocabulary and classifications."""
    
    def __init__(self):
        self._aesthetics_data: Optional[Dict] = None
        self._vocabulary: Optional[List[str]] = None
    
    async def initialize(self):
        """Initialize the service by loading aesthetics data."""
        try:
            await self._load_aesthetics_data()
            logger.info(f"Loaded {len(self._vocabulary)} aesthetic terms")
        except Exception as e:
            logger.error(f"Failed to initialize aesthetic service: {str(e)}")
            raise
    
    async def _load_aesthetics_data(self):
        """Load aesthetics data from YAML file."""
        aesthetics_file_path = settings.aesthetics_file
        if aesthetics_file_path is None:
            logger.error("❌ settings.aesthetics_file is None! Path resolution failed.")
            raise FileNotFoundError("Aesthetics file path is not configured")
        
        logger.info(f"📂 Attempting to load aesthetics from: {aesthetics_file_path}")
        logger.info(f"   File exists: {aesthetics_file_path.exists()}")
        logger.info(f"   Absolute path: {aesthetics_file_path.absolute()}")
        
        try:
            with open(aesthetics_file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                self._aesthetics_data = data.get('aesthetics', {})
                self._vocabulary = list(self._aesthetics_data.keys())
                logger.info(f"✅ Successfully loaded {len(self._vocabulary)} aesthetic terms")
        except FileNotFoundError as e:
            logger.error(f"❌ Aesthetics file not found: {aesthetics_file_path}")
            logger.error(f"   Absolute path: {aesthetics_file_path.absolute()}")
            logger.error(f"   Parent directory exists: {aesthetics_file_path.parent.exists()}")
            logger.error(f"   Parent directory contents: {list(aesthetics_file_path.parent.iterdir()) if aesthetics_file_path.parent.exists() else 'N/A'}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing aesthetics YAML: {str(e)}")
            raise
    
    async def get_all_aesthetics(self) -> Dict:
        """Get all available aesthetics with their data."""
        if self._aesthetics_data is None:
            await self._load_aesthetics_data()
        return self._aesthetics_data
    
    async def get_vocabulary(self) -> List[str]:
        """Get list of aesthetic terms for classification."""
        if self._vocabulary is None:
            await self._load_aesthetics_data()
        return self._vocabulary
    
    async def get_keywords_for_aesthetic(self, aesthetic: str) -> List[str]:
        """Get search keywords for a specific aesthetic."""
        if self._aesthetics_data is None:
            await self._load_aesthetics_data()
        
        aesthetic_data = self._aesthetics_data.get(aesthetic, {})
        return aesthetic_data.get('keywords', [])
    
    async def get_aesthetic_description(self, aesthetic: str) -> Optional[str]:
        """Get description for a specific aesthetic."""
        if self._aesthetics_data is None:
            await self._load_aesthetics_data()
        
        aesthetic_data = self._aesthetics_data.get(aesthetic, {})
        return aesthetic_data.get('description')
    
    async def get_negative_keywords_for_aesthetic(self, aesthetic: str) -> List[str]:
        """Get negative keywords to avoid for a specific aesthetic."""
        if self._aesthetics_data is None:
            await self._load_aesthetics_data()
        
        aesthetic_data = self._aesthetics_data.get(aesthetic, {})
        return aesthetic_data.get('negative_keywords', [])
    
    async def get_color_palette_for_aesthetic(self, aesthetic: str) -> List[str]:
        """Get preferred color palette for a specific aesthetic."""
        if self._aesthetics_data is None:
            await self._load_aesthetics_data()
        
        aesthetic_data = self._aesthetics_data.get(aesthetic, {})
        return aesthetic_data.get('color_palette', [])


# Global service instance
aesthetic_service = AestheticService()