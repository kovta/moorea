"""Flickr API client for fetching images."""

import logging
from typing import List, Optional, Dict, Any
import httpx
from urllib.parse import urlencode

from config import settings
from models import ImageCandidate

logger = logging.getLogger(__name__)


class FlickrClient:
    """Client for Flickr API integration."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.flickr_api_key
        self.base_url = "https://api.flickr.com/services/rest/"
        self.session = httpx.AsyncClient(timeout=30.0)
    
    async def search_photos(self, 
                          query: str, 
                          per_page: int = 20,
                          license_type: str = "4,5,6,7,8,9,10") -> List[ImageCandidate]:
        """
        Search for photos on Flickr.
        
        Args:
            query: Search term
            per_page: Number of results per page (max 500)
            license_type: Comma-separated license IDs (4-10 are Creative Commons)
        """
        if not self.api_key:
            logger.warning("Flickr API key not configured, skipping Flickr search")
            return []
        
        try:
            params = {
                'method': 'flickr.photos.search',
                'api_key': self.api_key,
                'text': query,
                'license': license_type,  # Only Creative Commons and public domain
                'content_type': '1',  # Photos only
                'media': 'photos',
                'per_page': min(per_page, 500),
                'page': 1,
                'format': 'json',
                'nojsoncallback': 1,
                'extras': 'url_m,url_c,owner_name,license',  # Medium and large URLs
                'sort': 'relevance',
                'safe_search': '1',  # Safe content only
            }
            
            response = await self.session.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('stat') != 'ok':
                logger.error(f"Flickr API error: {data.get('message', 'Unknown error')}")
                return []
            
            photos = data.get('photos', {}).get('photo', [])
            candidates = []
            
            for photo in photos:
                # Use medium or large size URL, fallback to construct URL
                image_url = photo.get('url_c') or photo.get('url_m')
                if not image_url:
                    # Construct URL manually if not provided
                    image_url = f"https://live.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}_c.jpg"
                
                # Thumbnail URL (small size)
                thumbnail_url = f"https://live.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}_m.jpg"
                
                # Flickr photo page URL
                flickr_page_url = f"https://www.flickr.com/photos/{photo.get('owner', '')}/{photo['id']}/"
                
                candidate = ImageCandidate(
                    id=f"flickr_{photo['id']}",
                    url=image_url,
                    thumbnail_url=thumbnail_url,
                    photographer=photo.get('ownername', 'Unknown'),
                    source_api="flickr",
                    source_url=flickr_page_url
                )
                candidates.append(candidate)
            
            logger.info(f"Flickr: Found {len(candidates)} images for '{query}'")
            return candidates
            
        except httpx.TimeoutException:
            logger.error(f"Flickr API timeout for query: {query}")
            return []
        except httpx.HTTPStatusError as e:
            logger.error(f"Flickr API HTTP error for query '{query}': {e}")
            return []
        except Exception as e:
            logger.error(f"Flickr API error for query '{query}': {str(e)}")
            return []
    
    async def get_photo_info(self, photo_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific photo."""
        if not self.api_key:
            return None
        
        try:
            params = {
                'method': 'flickr.photos.getInfo',
                'api_key': self.api_key,
                'photo_id': photo_id,
                'format': 'json',
                'nojsoncallback': 1,
            }
            
            response = await self.session.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if data.get('stat') == 'ok':
                return data.get('photo', {})
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting Flickr photo info for {photo_id}: {str(e)}")
            return None
    
    async def close(self):
        """Close the HTTP session."""
        await self.session.aclose()


# Global client instance
flickr_client = FlickrClient()
