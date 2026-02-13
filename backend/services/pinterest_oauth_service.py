import os
import secrets
from typing import Optional
import httpx
from fastapi import HTTPException
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

# Try to import Redis, but fall back to in-memory cache if unavailable
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class InMemoryCache:
    """Simple in-memory cache for development without Redis"""
    def __init__(self):
        self.store = {}

    def get(self, key: str) -> Optional[bytes]:
        value = self.store.get(key)
        if value is None:
            return None
        return value.encode() if isinstance(value, str) else value

    def set(self, key: str, value: str):
        """Store value as string (will be encoded on retrieval)"""
        self.store[key] = value if isinstance(value, str) else value.decode() if isinstance(value, bytes) else str(value)

    def setex(self, key: str, ttl: int, value: str):
        """Set with TTL (simplified - no actual expiration in memory cache)"""
        self.set(key, value)

    def delete(self, key: str):
        self.store.pop(key, None)


class PinterestOAuthService:
    """Pinterest OAuth 2.0 service for API authentication"""

    BASE_URL = "https://api.pinterest.com"
    AUTH_URL = "https://www.pinterest.com/oauth/"

    def __init__(self):
        self.client_id = settings.pinterest_client_id
        self.client_secret = settings.pinterest_client_secret
        self.client_key = settings.pinterest_client_key  # API key for direct authentication
        self.redirect_uri = settings.pinterest_redirect_uri

        # Initialize Redis client or fall back to in-memory cache
        try:
            if REDIS_AVAILABLE:
                self.redis_client = redis.from_url(settings.redis_url)
                self.redis_client.ping()  # Test connection
                logger.info("Redis connected successfully")
            else:
                raise Exception("Redis package not installed")
        except Exception as e:
            logger.warning(f"Redis unavailable ({e}), using in-memory cache for development")
            self.redis_client = InMemoryCache()

    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """Generate Pinterest authorization URL"""
        if not self.client_id:
            raise HTTPException(status_code=500, detail="Pinterest client_id not configured")

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

        # Filter out None values before building query string
        query_params = {k: v for k, v in params.items() if v is not None}
        query_string = "&".join(f"{k}={v}" for k, v in query_params.items())
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
        """Make authenticated API request with automatic token refresh or API key auth"""
        headers = kwargs.get("headers", {})

        # Try OAuth token first
        token = self.get_access_token()
        if token:
            headers["Authorization"] = f"Bearer {token}"
        # Fallback to API key authentication if configured
        elif self.client_key:
            headers["Authorization"] = f"Bearer {self.client_key}"
        else:
            raise HTTPException(status_code=401, detail="No valid Pinterest access token or API key configured")

        kwargs["headers"] = headers

        async with httpx.AsyncClient() as client:
            response = await client.request(method, f"{self.BASE_URL}{endpoint}", **kwargs)

            # If token expired, try refreshing once
            if response.status_code == 401 and not self.client_key:
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