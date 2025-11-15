"""reCAPTCHA verification service."""

import logging
import httpx
from typing import Optional
from config import settings

logger = logging.getLogger(__name__)


class RecaptchaService:
    """Service for verifying reCAPTCHA tokens with Google."""
    
    VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
    
    async def verify_token(self, token: str, remote_ip: Optional[str] = None) -> bool:
        """
        Verify a reCAPTCHA token with Google.
        
        Args:
            token: The reCAPTCHA token from the frontend
            remote_ip: Optional IP address of the user (for additional security)
            
        Returns:
            True if token is valid, False otherwise
        """
        if not settings.recaptcha_secret_key:
            logger.warning("⚠️ reCAPTCHA secret key not configured - skipping verification")
            return True  # Allow requests if reCAPTCHA is not configured
        
        if not token:
            logger.warning("⚠️ reCAPTCHA token is missing")
            return False
        
        try:
            data = {
                "secret": settings.recaptcha_secret_key,
                "response": token
            }
            
            if remote_ip:
                data["remoteip"] = remote_ip
            
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(self.VERIFY_URL, data=data)
                response.raise_for_status()
                result = response.json()
                
                success = result.get("success", False)
                
                if success:
                    logger.info("✅ reCAPTCHA verification successful")
                else:
                    error_codes = result.get("error-codes", [])
                    logger.warning(f"❌ reCAPTCHA verification failed: {error_codes}")
                
                return success
                
        except httpx.TimeoutException:
            logger.error("❌ reCAPTCHA verification timeout")
            return False
        except httpx.HTTPError as e:
            logger.error(f"❌ reCAPTCHA verification HTTP error: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ reCAPTCHA verification error: {str(e)}")
            return False


# Global service instance
recaptcha_service = RecaptchaService()

