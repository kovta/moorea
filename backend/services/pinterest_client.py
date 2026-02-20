"""Pinterest API client for fetching pins and images."""

import asyncio
from typing import List, Dict, Any, Optional
from urllib.parse import urlencode

from services.pinterest_oauth_service import pinterest_oauth
from models import ImageCandidate


class PinterestAPIClient:
    """Client for Pinterest REST API v5."""

    def __init__(self):
        self.oauth_service = pinterest_oauth

    async def search_pins(
        self,
        query: str,
        limit: int = 25,
        bookmark: Optional[str] = None
    ) -> Dict[str, Any]:
        """Search for pins using Pinterest API."""
        params = {
            "query": query,
            "limit": min(limit, 100)  # Pinterest API max is 100
        }

        if bookmark:
            params["bookmark"] = bookmark

        endpoint = f"/v5/search/pins?{urlencode(params)}"

        return await self.oauth_service.make_authenticated_request("GET", endpoint)

    async def get_pin_details(self, pin_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific pin."""
        endpoint = f"/v5/pins/{pin_id}"
        return await self.oauth_service.make_authenticated_request("GET", endpoint)

    async def get_user_pins(
        self,
        username: str,
        limit: int = 25,
        bookmark: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get pins from a specific user."""
        params = {"limit": min(limit, 100)}

        if bookmark:
            params["bookmark"] = bookmark

        query_string = f"?{urlencode(params)}" if params else ""
        endpoint = f"/v5/users/{username}/pins{query_string}"

        return await self.oauth_service.make_authenticated_request("GET", endpoint)

    async def search_and_extract_images(
        self,
        aesthetic_query: str,
        max_images: int = 20
    ) -> List[ImageCandidate]:
        """Search Pinterest for images matching an aesthetic and extract image data."""
        images = []
        bookmark = None
        import logging
        logger = logging.getLogger(__name__)

        while len(images) < max_images:
            try:
                # Search for pins
                logger.info(f"Searching Pinterest for '{aesthetic_query}', limit={min(25, max_images - len(images))}")
                search_results = await self.search_pins(
                    query=aesthetic_query,
                    limit=min(25, max_images - len(images)),
                    bookmark=bookmark
                )

                pins = search_results.get("items", [])
                logger.info(f"Pinterest search returned {len(pins)} pins for '{aesthetic_query}'")

                # Debug: log response structure when no pins found
                if not pins:
                    logger.warning(f"Pinterest returned 0 pins. Full response keys: {list(search_results.keys())}")
                    if "error" in search_results:
                        logger.error(f"Pinterest API error: {search_results.get('error')}")
                    if "message" in search_results:
                        logger.warning(f"Pinterest API message: {search_results.get('message')}")

                if not pins:
                    logger.info(f"No more pins available for '{aesthetic_query}'")
                    break

                # Extract image data from pins
                for pin in pins:
                    if len(images) >= max_images:
                        break

                    # Get the best image URL available
                    # Pinterest v5 API returns images under media.images with keys like "1200x", "600x", "150x150"
                    media = pin.get("media", {})
                    images_data = media.get("images", pin.get("images", {}))
                    image_url = None

                    # Try v5 API size keys first, then v3 fallbacks
                    preferred_sizes = ["1200x", "600x", "400x300", "236x", "150x150", "original", "564x", "136x"]
                    for size in preferred_sizes:
                        if size in images_data:
                            entry = images_data[size]
                            if isinstance(entry, dict) and "url" in entry:
                                image_url = entry["url"]
                                break
                    # Last resort: take the first available image entry
                    if not image_url and images_data:
                        first = next(iter(images_data.values()), None)
                        if isinstance(first, dict):
                            image_url = first.get("url")

                    if not image_url:
                        logger.debug(f"Pinterest pin {pin.get('id')} has no extractable image. media keys: {list(images_data.keys())}")

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
                        images.append(candidate)

                # Check for next page
                bookmark = search_results.get("bookmark")
                if not bookmark:
                    break

                # Small delay to be respectful to the API
                await asyncio.sleep(0.1)

            except Exception as e:
                logger.error(f"Error fetching Pinterest images for '{aesthetic_query}': {str(e)}", exc_info=True)
                break

        return images

    async def is_authenticated(self) -> bool:
        """Check if Pinterest API is authenticated (has access or refresh token)."""
        has_access = self.oauth_service.get_access_token() is not None
        has_refresh = self.oauth_service.redis_client.get("pinterest_refresh_token") is not None
        return has_access or has_refresh


# Global Pinterest API client instance
pinterest_client = PinterestAPIClient()
