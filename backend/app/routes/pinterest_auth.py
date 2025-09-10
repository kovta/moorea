"""
Pinterest OAuth Authentication Routes
Handles Pinterest OAuth flow endpoints
"""
from fastapi import APIRouter, HTTPException, Query, Request, Depends
from fastapi.responses import RedirectResponse, JSONResponse
import logging
from typing import Optional
import secrets
import asyncio

from services.pinterest_client import pinterest_client, PinterestTokens
from models import APIResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth/pinterest", tags=["Pinterest OAuth"])

# In-memory session store (replace with Redis/database in production)
oauth_sessions = {}
user_tokens = {}  # Store user tokens (replace with database)

@router.get("/authorize")
async def pinterest_authorize(user_id: Optional[str] = Query(None)):
    """
    Initiate Pinterest OAuth flow
    Redirects user to Pinterest authorization page
    """
    try:
        # Generate unique state for CSRF protection
        state = secrets.token_urlsafe(32)
        
        # Store session data (replace with proper session management)
        oauth_sessions[state] = {
            "user_id": user_id,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # Generate Pinterest authorization URL
        auth_url = pinterest_client.get_authorization_url(state=state)
        
        logger.info(f"Redirecting to Pinterest OAuth for user: {user_id}")
        return RedirectResponse(url=auth_url)
    
    except Exception as e:
        logger.error(f"Pinterest authorization failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate Pinterest authorization")

@router.get("/callback")
async def pinterest_callback(
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    error: Optional[str] = Query(None)
):
    """
    Pinterest OAuth callback endpoint
    Handles the response from Pinterest after user authorization
    """
    try:
        # Handle authorization errors
        if error:
            logger.error(f"Pinterest OAuth error: {error}")
            return RedirectResponse(
                url=f"http://localhost:3000/auth/error?error={error}",
                status_code=302
            )
        
        # Validate required parameters
        if not code or not state:
            logger.error("Missing code or state parameter in Pinterest callback")
            return RedirectResponse(
                url="http://localhost:3000/auth/error?error=missing_parameters",
                status_code=302
            )
        
        # Validate state (CSRF protection)
        session_data = oauth_sessions.get(state)
        if not session_data:
            logger.error(f"Invalid or expired state parameter: {state}")
            return RedirectResponse(
                url="http://localhost:3000/auth/error?error=invalid_state",
                status_code=302
            )
        
        # Clean up session
        del oauth_sessions[state]
        
        # Exchange authorization code for tokens
        tokens = await pinterest_client.exchange_code_for_tokens(code)
        
        # Store tokens (replace with proper user session/database)
        user_id = session_data.get("user_id", "anonymous")
        user_tokens[user_id] = tokens.dict()
        
        logger.info(f"Successfully obtained Pinterest tokens for user: {user_id}")
        
        # Redirect to frontend success page with user_id
        return RedirectResponse(
            url=f"http://localhost:3000/auth/success?service=pinterest&user_id={user_id}",
            status_code=302
        )
    
    except Exception as e:
        logger.error(f"Pinterest callback failed: {e}")
        return RedirectResponse(
            url=f"http://localhost:3000/auth/error?error=callback_failed&details={str(e)}",
            status_code=302
        )

@router.get("/status/{user_id}")
async def pinterest_status(user_id: str):
    """Check Pinterest authentication status for a user"""
    try:
        tokens = user_tokens.get(user_id)
        if not tokens:
            return APIResponse(
                status="not_authenticated",
                message="User not authenticated with Pinterest"
            )
        
        # Test if tokens are still valid by making a simple API call
        try:
            boards = await pinterest_client.get_user_boards(tokens["access_token"])
            return APIResponse(
                status="authenticated",
                message="Pinterest authentication active",
                data={
                    "boards_count": len(boards),
                    "has_boards": len(boards) > 0
                }
            )
        except Exception as api_error:
            logger.warning(f"Pinterest tokens may be expired for user {user_id}: {api_error}")
            return APIResponse(
                status="token_expired",
                message="Pinterest authentication expired, please re-authenticate"
            )
    
    except Exception as e:
        logger.error(f"Pinterest status check failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to check Pinterest status")

@router.get("/boards/{user_id}")
async def get_pinterest_boards(user_id: str):
    """Get user's Pinterest boards"""
    try:
        tokens = user_tokens.get(user_id)
        if not tokens:
            raise HTTPException(status_code=401, detail="Not authenticated with Pinterest")
        
        boards = await pinterest_client.get_user_boards(tokens["access_token"])
        
        return APIResponse(
            status="success",
            message=f"Retrieved {len(boards)} Pinterest boards",
            data={
                "boards": [board.dict() for board in boards]
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get Pinterest boards: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve Pinterest boards")

@router.post("/save-moodboard/{user_id}")
async def save_moodboard_to_pinterest(
    user_id: str,
    request: Request
):
    """Save generated moodboard to Pinterest as a pin"""
    try:
        tokens = user_tokens.get(user_id)
        if not tokens:
            raise HTTPException(status_code=401, detail="Not authenticated with Pinterest")
        
        # Parse request body
        body = await request.json()
        board_id = body.get("board_id")
        title = body.get("title", "AI Generated Moodboard")
        description = body.get("description", "Created with AI fashion classification")
        image_url = body.get("image_url")  # URL of the generated moodboard image
        link = body.get("link")  # Optional link back to your app
        
        if not board_id or not image_url:
            raise HTTPException(
                status_code=400, 
                detail="board_id and image_url are required"
            )
        
        # Create pin on Pinterest
        pin = await pinterest_client.create_pin(
            access_token=tokens["access_token"],
            board_id=board_id,
            title=title,
            description=description,
            image_url=image_url,
            link=link
        )
        
        logger.info(f"Successfully saved moodboard to Pinterest: {pin.id}")
        
        return APIResponse(
            status="success",
            message="Moodboard saved to Pinterest successfully",
            data={
                "pin": pin.dict()
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to save moodboard to Pinterest: {e}")
        raise HTTPException(status_code=500, detail="Failed to save moodboard to Pinterest")

@router.post("/search-pins/{user_id}")
async def search_pinterest_pins(
    user_id: str,
    request: Request
):
    """Search Pinterest pins for moodboard inspiration"""
    try:
        tokens = user_tokens.get(user_id)
        if not tokens:
            raise HTTPException(status_code=401, detail="Not authenticated with Pinterest")
        
        body = await request.json()
        query = body.get("query")
        limit = body.get("limit", 20)
        
        if not query:
            raise HTTPException(status_code=400, detail="Search query is required")
        
        pins = await pinterest_client.search_pins(
            access_token=tokens["access_token"],
            query=query,
            limit=limit
        )
        
        return APIResponse(
            status="success",
            message=f"Found {len(pins)} Pinterest pins",
            data={
                "pins": pins,
                "query": query,
                "count": len(pins)
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Pinterest pin search failed: {e}")
        raise HTTPException(status_code=500, detail="Pinterest search failed")

@router.delete("/disconnect/{user_id}")
async def disconnect_pinterest(user_id: str):
    """Disconnect user's Pinterest account"""
    try:
        if user_id in user_tokens:
            del user_tokens[user_id]
            logger.info(f"Disconnected Pinterest for user: {user_id}")
        
        return APIResponse(
            status="success",
            message="Pinterest account disconnected"
        )
    
    except Exception as e:
        logger.error(f"Failed to disconnect Pinterest: {e}")
        raise HTTPException(status_code=500, detail="Failed to disconnect Pinterest")
