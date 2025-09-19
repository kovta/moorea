"""Unsplash API client for fetching images."""

import logging
from typing import List, Optional
import httpx

from config import settings
from models import ImageCandidate
from services.cache_service import cache_service

logger = logging.getLogger(__name__)


class UnsplashClient:
    """Client for Unsplash API integration."""
    
    def __init__(self, access_key: Optional[str] = None):
        self.access_key = access_key or settings.unsplash_access_key
        self.base_url = "https://api.unsplash.com"
        self.session = httpx.AsyncClient(
            timeout=5.0,  # Reduced from 30s to 5s for faster response
            headers={
                "Authorization": f"Client-ID {self.access_key}" if self.access_key else ""
            }
        )
    
    async def search_photos(self, query: str, per_page: int = 20) -> List[ImageCandidate]:
        """Search for photos on Unsplash."""
        if not self.access_key:
            logger.warning("Unsplash access key not configured, skipping Unsplash search")
            return []
        
        # Check cache first
        cached_result = await cache_service.get_api_cache("unsplash", f"{query}:{per_page}")
        if cached_result:
            return [ImageCandidate(**item) for item in cached_result]
        
        try:
            params = {
                'query': query,
                'per_page': min(per_page, 30),  # Unsplash max is 30
                'order_by': 'relevant',
                'content_filter': 'high',
                'orientation': 'all'
            }
            
            response = await self.session.get(f"{self.base_url}/search/photos", params=params)
            response.raise_for_status()
            
            data = response.json()
            photos = data.get('results', [])
            
            candidates = []
            for photo in photos:
                urls = photo.get('urls', {})
                user = photo.get('user', {})
                links = photo.get('links', {})
                
                candidate = ImageCandidate(
                    id=f"unsplash_{photo['id']}",
                    url=urls.get('regular', urls.get('small', '')),
                    thumbnail_url=urls.get('thumb', urls.get('small', '')),
                    photographer=user.get('name', 'Unknown'),
                    source_api="unsplash",
                    download_location=links.get('download_location')
                )
                candidates.append(candidate)
            
            logger.info(f"Unsplash: Found {len(candidates)} images for '{query}'")
            
            # Cache the result
            candidate_dicts = [candidate.dict() for candidate in candidates]
            await cache_service.set_api_cache("unsplash", f"{query}:{per_page}", candidate_dicts)
            
            return candidates
            
        except httpx.TimeoutException:
            logger.error(f"Unsplash API timeout for query: {query}")
            return []
        except httpx.HTTPStatusError as e:
            logger.error(f"Unsplash API HTTP error for query '{query}': {e}")
            return []
        except Exception as e:
            logger.error(f"Unsplash API error for query '{query}': {str(e)}")
            return []
    
    async def trigger_download_event(self, download_location: str) -> bool:
        """Trigger download event for Unsplash tracking compliance."""
        if not self.access_key or not download_location:
            return False
        
        try:
            response = await self.session.get(download_location)
            response.raise_for_status()
            logger.info(f"Unsplash download event triggered successfully: {download_location}")
            return True
            
        except httpx.HTTPStatusError as e:
            logger.error(f"Unsplash download tracking HTTP error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unsplash download tracking error: {str(e)}")
            return False
    
    async def trigger_download_events(self, images: List[ImageCandidate]) -> int:
        """Trigger download events for multiple Unsplash images."""
        success_count = 0
        
        for image in images:
            if image.source_api == "unsplash" and image.download_location:
                success = await self.trigger_download_event(image.download_location)
                if success:
                    success_count += 1
        
        if success_count > 0:
            logger.info(f"Successfully triggered {success_count} Unsplash download events")
        
        return success_count
    
    async def close(self):
        """Close the HTTP session."""
        await self.session.aclose()


# Global client instance
unsplash_client = UnsplashClient()