"""Pinterest OAuth routes for API integration."""

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
from typing import Optional
import secrets
import logging

from services.pinterest_oauth_service import pinterest_oauth
from config.settings import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/auth/pinterest", tags=["pinterest-oauth"])

@router.get("/authorize")
async def authorize_pinterest():
    """Initiate Pinterest OAuth authorization flow - redirect to authorization URL."""
    try:
        logger.info(f"Authorize endpoint called. pinterest_oauth is None: {pinterest_oauth is None}")
        if not pinterest_oauth:
            logger.error("Pinterest OAuth service is not initialized")
            raise HTTPException(status_code=500, detail="Pinterest OAuth service not initialized")
        auth_url = pinterest_oauth.get_authorization_url()
        logger.info(f"Generated auth URL: {auth_url}")
        
        # Return a redirect response (not JSON)
        # This is the correct OAuth 2.0 flow - redirect browser to authorization endpoint
        return RedirectResponse(url=auth_url, status_code=302)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in authorize: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to generate authorization URL: {str(e)}")

@router.get("/mock-authorize")
async def mock_authorize_pinterest(state: str = Query(...)):
    """Mock authorization endpoint for testing - simulates Pinterest redirect."""
    if settings.use_mock_pinterest:
        # Generate a mock authorization code
        mock_code = "mock_code_" + secrets.token_urlsafe(16)
        
        # Redirect to callback with mock code and state
        callback_url = f"{settings.pinterest_redirect_uri}?code={mock_code}&state={state}"
        return RedirectResponse(url=callback_url)
    else:
        raise HTTPException(status_code=400, detail="Mock authorize endpoint only available when USE_MOCK_PINTEREST=true")

@router.get("/callback")
async def pinterest_oauth_callback(
    code: str = Query(..., description="Authorization code from Pinterest"),
    state: str = Query(..., description="State parameter for CSRF protection")
):
    """Handle Pinterest OAuth callback and exchange code for token."""
    try:
        token_data = await pinterest_oauth.exchange_code_for_token(code, state)

        # Return success response (you might want to redirect to frontend)
        return {
            "message": "Pinterest authorization successful",
            "access_token_expires_in": token_data.get("expires_in"),
            "scope": token_data.get("scope")
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OAuth callback failed: {str(e)}")

@router.get("/status")
async def check_pinterest_auth_status():
    """Check if Pinterest is currently authenticated."""
    token = pinterest_oauth.get_access_token()
    return {
        "authenticated": token is not None,
        "has_token": bool(token)
    }

@router.post("/refresh")
async def refresh_pinterest_token():
    """Manually refresh Pinterest access token."""
    try:
        new_token = await pinterest_oauth.refresh_access_token()
        if new_token:
            return {"message": "Token refreshed successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to refresh token - no refresh token available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token refresh failed: {str(e)}")


@router.get("/search")
async def search_pinterest(query: str = Query(..., description="Search query for pins")):
    """Search Pinterest for pins matching the given aesthetic query."""
    try:
        # Use authenticated request to search Pinterest
        response = await pinterest_oauth.make_authenticated_request(
            "GET",
            f"/v5/search/pins?query={query}&limit=30"
        )
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pinterest search failed: {str(e)}")