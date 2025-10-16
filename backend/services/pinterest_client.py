"""Pinterest API client for fetching pins and boards."""

import asyncio
import logging
from typing import List, Optional, Dict, Any
import aiohttp
from models import ImageCandidate

logger = logging.getLogger(__name__)


class PinterestClient:
    """Pinterest API client for fetching pins and boards."""
    
    def __init__(self, access_token: str):
        """Initialize Pinterest client with access token."""
        self.access_token = access_token
        self.base_url = "https://api.pinterest.com/v5"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    async def search_pins(self, query: str, limit: int = 10) -> List[ImageCandidate]:
        """Search for pins based on query."""
        try:
            url = f"{self.base_url}/search/pins"
            params = {
                "query": query,
                "limit": limit,
                "bookmark": None
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        pins = data.get("items", [])
                        
                        candidates = []
                        for pin in pins:
                            # Extract image URL from pin
                            image_url = None
                            if "media" in pin and "images" in pin["media"]:
                                images = pin["media"]["images"]
                                # Try to get the best quality image
                                if "564x" in images:
                                    image_url = images["564x"]["url"]
                                elif "736x" in images:
                                    image_url = images["736x"]["url"]
                                elif "originals" in images:
                                    image_url = images["originals"]["url"]
                            
                            if image_url:
                                candidate = ImageCandidate(
                                    id=pin.get("id", ""),
                                    url=image_url,
                                    photographer=pin.get("creator", {}).get("username", "Pinterest User"),
                                    source_api="pinterest",
                                    pinterest_url=pin.get("url", ""),
                                    pinterest_board=pin.get("board_name", ""),
                                    title=pin.get("title", ""),
                                    description=pin.get("description", "")
                                )
                                candidates.append(candidate)
                        
                        logger.info(f"✅ Pinterest: Found {len(candidates)} pins for query '{query}'")
                        return candidates
                    
                    else:
                        logger.warning(f"⚠️ Pinterest API error: {response.status} - {await response.text()}")
                        return []
                        
        except Exception as e:
            logger.error(f"❌ Pinterest search error: {str(e)}")
            return []
    
    async def get_board_pins(self, board_id: str, limit: int = 10) -> List[ImageCandidate]:
        """Get pins from a specific board."""
        try:
            url = f"{self.base_url}/boards/{board_id}/pins"
            params = {
                "limit": limit,
                "bookmark": None
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        pins = data.get("items", [])
                        
                        candidates = []
                        for pin in pins:
                            # Extract image URL from pin
                            image_url = None
                            if "media" in pin and "images" in pin["media"]:
                                images = pin["media"]["images"]
                                # Try to get the best quality image
                                if "564x" in images:
                                    image_url = images["564x"]["url"]
                                elif "736x" in images:
                                    image_url = images["736x"]["url"]
                                elif "originals" in images:
                                    image_url = images["originals"]["url"]
                            
                            if image_url:
                                candidate = ImageCandidate(
                                    id=pin.get("id", ""),
                                    url=image_url,
                                    photographer=pin.get("creator", {}).get("username", "Pinterest User"),
                                    source_api="pinterest",
                                    pinterest_url=pin.get("url", ""),
                                    pinterest_board=pin.get("board_name", ""),
                                    title=pin.get("title", ""),
                                    description=pin.get("description", "")
                                )
                                candidates.append(candidate)
                        
                        logger.info(f"✅ Pinterest: Found {len(candidates)} pins from board '{board_id}'")
                        return candidates
                    
                    else:
                        logger.warning(f"⚠️ Pinterest API error: {response.status} - {await response.text()}")
                        return []
                        
        except Exception as e:
            logger.error(f"❌ Pinterest board error: {str(e)}")
            return []
    
    async def test_connection(self) -> bool:
        """Test Pinterest API connection."""
        try:
            url = f"{self.base_url}/user_account"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        username = data.get("username", "Unknown")
                        logger.info(f"✅ Pinterest API connected successfully! User: {username}")
                        return True
                    else:
                        logger.warning(f"⚠️ Pinterest API connection failed: {response.status}")
                        return False
                        
        except Exception as e:
            logger.error(f"❌ Pinterest connection test error: {str(e)}")
            return False


# Global Pinterest client instance
pinterest_client: Optional[PinterestClient] = None


def initialize_pinterest_client(access_token: str) -> PinterestClient:
    """Initialize the global Pinterest client."""
    global pinterest_client
    pinterest_client = PinterestClient(access_token)
    return pinterest_client


def get_pinterest_client() -> Optional[PinterestClient]:
    """Get the global Pinterest client instance."""
    return pinterest_client
