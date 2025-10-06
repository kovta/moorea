"""Pexels API client for fetching images."""

import logging
from typing import List, Optional
import httpx

from config import settings
from models import ImageCandidate

logger = logging.getLogger(__name__)


class PexelsClient:
    """Client for Pexels API integration."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.pexels_api_key
        self.base_url = "https://api.pexels.com/v1"
        self.session = httpx.AsyncClient(
            timeout=5.0,  # Reduced from 30s to 5s for faster response
            headers={
                "Authorization": self.api_key if self.api_key else ""
            }
        )
    
    async def search_photos(self, query: str, per_page: int = 20) -> List[ImageCandidate]:
        """Search for photos on Pexels."""
        if not self.api_key:
            logger.warning("Pexels API key not configured, skipping Pexels search")
            return []
        
        try:
            params = {
                'query': query,
                'per_page': min(per_page, 80),  # Pexels max is 80
                'page': 1,
                'orientation': 'all',
                'size': 'all'
            }
            
            response = await self.session.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            
            data = response.json()
            photos = data.get('photos', [])
            
            candidates = []
            for photo in photos:
                src = photo.get('src', {})
                
                candidate = ImageCandidate(
                    id=f"pexels_{photo['id']}",
                    url=src.get('large2x', src.get('large', src.get('medium', ''))),
                    thumbnail_url=src.get('medium', src.get('small', '')),
                    photographer=photo.get('photographer', 'Unknown'),
                    source_api="pexels",
                    source_url=photo.get('url', f"https://www.pexels.com/photo/{photo['id']}/")
                )
                candidates.append(candidate)
            
            logger.info(f"Pexels: Found {len(candidates)} images for '{query}'")
            return candidates
            
        except httpx.TimeoutException:
            logger.error(f"Pexels API timeout for query: {query}")
            return []
        except httpx.HTTPStatusError as e:
            logger.error(f"Pexels API HTTP error for query '{query}': {e}")
            return []
        except Exception as e:
            logger.error(f"Pexels API error for query '{query}': {str(e)}")
            return []
    
    async def close(self):
        """Close the HTTP session."""
        await self.session.aclose()


# Global client instance
pexels_client = PexelsClient()
