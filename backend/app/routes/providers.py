"""Provider status endpoints."""

import logging
from fastapi import APIRouter

from config import settings
from models import HealthResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/providers/status")
async def providers_status():
    """Report configured provider keys and Pinterest auth state."""
    status = {
        "unsplash_configured": bool(settings.unsplash_access_key),
        "pexels_configured": bool(settings.pexels_api_key),
        "flickr_configured": bool(settings.flickr_api_key),
        "pinterest_mock_enabled": bool(settings.use_mock_pinterest),
    }

    # Try to report Pinterest auth state if client is available
    try:
        from services.pinterest_client import pinterest_client
        is_auth = await pinterest_client.is_authenticated()
        status["pinterest_authenticated"] = bool(is_auth)
    except Exception as e:
        status["pinterest_authenticated"] = False
        logger.warning(f"Pinterest client unavailable: {e}")

    return status
