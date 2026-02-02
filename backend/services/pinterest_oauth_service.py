import os
import secrets
from typing import Optional
import httpx
from fastapi import HTTPException
import redis
from config.settings import settings


class PinterestOAuthService:
    """Pinterest OAuth 2.0 service for API authentication"""

    BASE_URL = "https://api.pinterest.com"
    AUTH_URL = "https://www.pinterest.com/oauth/"

    def __init__(self):
        self.client_id = settings.pinterest_client_id
        self.client_secret = settings.pinterest_client_secret
        self.redirect_uri = settings.pinterest_redirect_uri
        self.redis_client = redis.from_url(settings.redis_url)

    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """Generate Pinterest authorization URL"""
        if not state:
            state = secrets.token_urlsafe(32)

        # Store state in Redis for verification (5 minute expiry)
        self.redis_client.setex(f"pinterest_oauth_state:{state}", 300, "valid")

        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": "pins:read",  # Adjust scopes as needed
            "state": state
        }

        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        return f"{self.AUTH_URL}?{query_string}"

    async def exchange_code_for_token(self, code: str, state: str) -> dict:
        """Exchange authorization code for access token"""
        # Verify state
        stored_state = self.redis_client.get(f"pinterest_oauth_state:{state}")
        if not stored_state:
            raise HTTPException(status_code=400, detail="Invalid or expired state")

        # Remove used state
        self.redis_client.delete(f"pinterest_oauth_state:{state}")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/v5/oauth/token",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": self.redirect_uri
                },
                auth=(self.client_id, self.client_secret)
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=400,
                    detail=f"Token exchange failed: {response.text}"
                )

            token_data = response.json()

            # Store token in Redis (with expiry)
            access_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 2592000)  # 30 days default

            self.redis_client.setex(
                "pinterest_access_token",
                expires_in,
                access_token
            )

            if "refresh_token" in token_data:
                self.redis_client.set(
                    "pinterest_refresh_token",
                    token_data["refresh_token"]
                )

            return token_data

    async def refresh_access_token(self) -> Optional[str]:
        """Refresh expired access token"""
        refresh_token = self.redis_client.get("pinterest_refresh_token")

        if not refresh_token:
            return None

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/v5/oauth/token",
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token
                },
                auth=(self.client_id, self.client_secret)
            )

            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data["access_token"]
                expires_in = token_data.get("expires_in", 2592000)

                self.redis_client.setex(
                    "pinterest_access_token",
                    expires_in,
                    access_token
                )

                return access_token

        return None

    def get_access_token(self) -> Optional[str]:
        """Get current access token"""
        token = self.redis_client.get("pinterest_access_token")
        return token.decode() if token else None

    async def make_authenticated_request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make authenticated API request with automatic token refresh"""
        token = self.get_access_token()

        if not token:
            # Try to refresh token
            token = await self.refresh_access_token()
            if not token:
                raise HTTPException(status_code=401, detail="No valid Pinterest access token")

        headers = kwargs.get("headers", {})
        headers["Authorization"] = f"Bearer {token}"
        kwargs["headers"] = headers

        async with httpx.AsyncClient() as client:
            response = await client.request(method, f"{self.BASE_URL}{endpoint}", **kwargs)

            # If token expired, try refreshing once
            if response.status_code == 401:
                new_token = await self.refresh_access_token()
                if new_token:
                    headers["Authorization"] = f"Bearer {new_token}"
                    response = await client.request(method, f"{self.BASE_URL}{endpoint}", **kwargs)

            if response.status_code >= 400:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Pinterest API error: {response.text}"
                )

            return response.json()

# Global service instance - use mock or real based on settings
try:
    if settings.use_mock_pinterest:
        from .mock_pinterest_service import mock_pinterest_oauth
        pinterest_oauth = mock_pinterest_oauth
        if pinterest_oauth is None:
            import logging
            logger = logging.getLogger(__name__)
            logger.error("Mock Pinterest OAuth service failed to initialize")
    else:
        pinterest_oauth = PinterestOAuthService()
except Exception as e:
    import logging
    logger = logging.getLogger(__name__)
    logger.error(f"Failed to initialize Pinterest OAuth service: {str(e)}", exc_info=True)
    pinterest_oauth = None