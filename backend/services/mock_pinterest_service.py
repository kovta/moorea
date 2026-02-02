"""Mock Pinterest OAuth service for development/testing without real API credentials."""

import secrets
from typing import Optional
import redis
import logging
from config.settings import settings

logger = logging.getLogger(__name__)


class MockPinterestOAuthService:
    """Mock Pinterest OAuth 2.0 service that simulates API responses"""

    def __init__(self):
        self.redis_client = redis.from_url(settings.redis_url)
        self.mock_access_token = "mock_access_token_" + secrets.token_urlsafe(16)

    def get_authorization_url(self, state: Optional[str] = None) -> str:
        """Generate mock Pinterest authorization URL"""
        if not state:
            state = secrets.token_urlsafe(32)

        # Store state in Redis for verification (5 minute expiry)
        state_key = f"pinterest_oauth_state:{state}"
        self.redis_client.setex(state_key, 300, "valid")
        logger.info(f"Stored OAuth state in Redis: {state_key}")

        # Simulate Pinterest authorization URL - points to backend mock-authorize endpoint
        mock_auth_url = f"{settings.backend_url}/api/v1/auth/pinterest/mock-authorize?state={state}"
        return mock_auth_url

    async def exchange_code_for_token(self, code: str, state: str) -> dict:
        """Exchange mock authorization code for mock access token"""
        # Verify state
        state_key = f"pinterest_oauth_state:{state}"
        stored_state = self.redis_client.get(state_key)
        logger.info(f"Attempting to verify state: {state_key}")
        logger.info(f"State found in Redis: {stored_state}")
        if not stored_state:
            raise ValueError("Invalid or expired state")

        # Remove used state
        self.redis_client.delete(f"pinterest_oauth_state:{state}")

        # Simulate token response
        token_data = {
            "access_token": self.mock_access_token,
            "token_type": "Bearer",
            "expires_in": 2592000,  # 30 days
            "refresh_token": "mock_refresh_token_" + secrets.token_urlsafe(16),
            "scope": "pins:read boards:read"
        }

        # Store token in Redis (with expiry)
        expires_in = token_data.get("expires_in", 2592000)

        self.redis_client.setex(
            "pinterest_access_token",
            expires_in,
            token_data["access_token"]
        )

        if "refresh_token" in token_data:
            self.redis_client.set(
                "pinterest_refresh_token",
                token_data["refresh_token"]
            )

        return token_data

    async def refresh_access_token(self) -> Optional[str]:
        """Refresh mock access token"""
        refresh_token = self.redis_client.get("pinterest_refresh_token")

        if not refresh_token:
            return None

        # Generate new mock token
        new_token = "mock_access_token_" + secrets.token_urlsafe(16)
        expires_in = 2592000

        self.redis_client.setex(
            "pinterest_access_token",
            expires_in,
            new_token
        )

        self.mock_access_token = new_token
        return new_token

    def get_access_token(self) -> Optional[str]:
        """Get current mock access token"""
        token = self.redis_client.get("pinterest_access_token")
        return token.decode() if token else None

    async def make_authenticated_request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make mock authenticated API request"""
        token = self.get_access_token()

        if not token:
            # Try to refresh token
            token = await self.refresh_access_token()
            if not token:
                raise ValueError("No valid mock Pinterest access token")

        # Return mock data based on endpoint
        if "search" in endpoint or "pins" in endpoint:
            return self._get_mock_pins_response()

        return {"message": "Mock response", "status": "success"}

    @staticmethod
    def _get_mock_pins_response() -> dict:
        """Generate mock Pinterest pins response"""
        return {
            "items": [
                {
                    "id": f"mock_pin_{i}",
                    "url": f"https://via.placeholder.com/400x500?text=Pin+{i+1}",
                    "title": f"Mock Pin {i+1}",
                    "description": f"This is a mock Pinterest pin for testing ({i+1})",
                    "created_at": "2024-01-01T00:00:00Z"
                }
                for i in range(15)
            ],
            "page_size": 15,
            "bookmark": None
        }


# Global mock service instance
try:
    mock_pinterest_oauth = MockPinterestOAuthService()
except Exception as e:
    logger.error(f"Failed to initialize mock Pinterest OAuth service: {str(e)}", exc_info=True)
    mock_pinterest_oauth = None
