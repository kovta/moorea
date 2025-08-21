"""Redis caching service for performance optimization."""

import json
import logging
import hashlib
from typing import Optional, Any, Dict, List
import numpy as np
import redis.asyncio as redis
from datetime import datetime, timedelta

from config import settings

logger = logging.getLogger(__name__)


class CacheService:
    """Service for Redis-based caching."""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self._connected = False
    
    async def initialize(self):
        """Initialize Redis connection."""
        try:
            self.redis_client = redis.from_url(
                settings.redis_url,
                encoding="utf-8",
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            
            # Test connection
            await self.redis_client.ping()
            self._connected = True
            logger.info("Redis cache initialized successfully")
            
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {str(e)}. Caching disabled.")
            self._connected = False
    
    def _generate_cache_key(self, prefix: str, data: Any) -> str:
        """Generate consistent cache key."""
        if isinstance(data, bytes):
            # For image data, use hash
            content_hash = hashlib.sha256(data).hexdigest()[:16]
            return f"{prefix}:{content_hash}"
        elif isinstance(data, str):
            return f"{prefix}:{data}"
        else:
            # For complex objects, serialize and hash
            serialized = json.dumps(data, sort_keys=True)
            content_hash = hashlib.sha256(serialized.encode()).hexdigest()[:16]
            return f"{prefix}:{content_hash}"
    
    async def get_classification_cache(self, image_content: bytes) -> Optional[List[Dict]]:
        """Get cached aesthetic classification."""
        if not self._connected:
            return None
        
        try:
            key = self._generate_cache_key("classification", image_content)
            cached_data = await self.redis_client.get(key)
            
            if cached_data:
                logger.debug(f"Cache hit for classification: {key}")
                return json.loads(cached_data)
            
            return None
            
        except Exception as e:
            logger.warning(f"Cache get error: {str(e)}")
            return None
    
    async def set_classification_cache(self, image_content: bytes, classification_result: List[Dict]) -> None:
        """Cache aesthetic classification result."""
        if not self._connected:
            return
        
        try:
            key = self._generate_cache_key("classification", image_content)
            
            await self.redis_client.setex(
                key,
                settings.classification_cache_ttl,
                json.dumps(classification_result)
            )
            
            logger.debug(f"Cached classification: {key}")
            
        except Exception as e:
            logger.warning(f"Cache set error: {str(e)}")
    
    async def get_api_cache(self, api_name: str, query: str) -> Optional[List[Dict]]:
        """Get cached API response."""
        if not self._connected:
            return None
        
        try:
            key = self._generate_cache_key(f"api:{api_name}", query)
            cached_data = await self.redis_client.get(key)
            
            if cached_data:
                logger.debug(f"API cache hit: {api_name}:{query}")
                return json.loads(cached_data)
            
            return None
            
        except Exception as e:
            logger.warning(f"API cache get error: {str(e)}")
            return None
    
    async def set_api_cache(self, api_name: str, query: str, api_result: List[Dict]) -> None:
        """Cache API response."""
        if not self._connected:
            return
        
        try:
            key = self._generate_cache_key(f"api:{api_name}", query)
            
            await self.redis_client.setex(
                key,
                settings.api_cache_ttl,
                json.dumps(api_result)
            )
            
            logger.debug(f"Cached API response: {api_name}:{query}")
            
        except Exception as e:
            logger.warning(f"API cache set error: {str(e)}")
    
    async def get_embedding_cache(self, image_url: str) -> Optional[np.ndarray]:
        """Get cached image embedding."""
        if not self._connected:
            return None
        
        try:
            key = self._generate_cache_key("embedding", image_url)
            cached_data = await self.redis_client.get(key)
            
            if cached_data:
                # Embeddings are stored as JSON arrays
                embedding_list = json.loads(cached_data)
                return np.array(embedding_list, dtype=np.float32)
            
            return None
            
        except Exception as e:
            logger.warning(f"Embedding cache get error: {str(e)}")
            return None
    
    async def set_embedding_cache(self, image_url: str, embedding: np.ndarray) -> None:
        """Cache image embedding."""
        if not self._connected:
            return
        
        try:
            key = self._generate_cache_key("embedding", image_url)
            
            # Convert numpy array to list for JSON serialization
            embedding_list = embedding.tolist()
            
            await self.redis_client.setex(
                key,
                settings.embedding_cache_ttl,
                json.dumps(embedding_list)
            )
            
            logger.debug(f"Cached embedding: {image_url}")
            
        except Exception as e:
            logger.warning(f"Embedding cache set error: {str(e)}")
    
    async def get_moodboard_cache(self, image_hash: str) -> Optional[Dict]:
        """Get cached complete moodboard."""
        if not self._connected:
            return None
        
        try:
            key = self._generate_cache_key("moodboard", image_hash)
            cached_data = await self.redis_client.get(key)
            
            if cached_data:
                logger.debug(f"Moodboard cache hit: {image_hash}")
                return json.loads(cached_data)
            
            return None
            
        except Exception as e:
            logger.warning(f"Moodboard cache get error: {str(e)}")
            return None
    
    async def set_moodboard_cache(self, image_hash: str, moodboard_result: Dict) -> None:
        """Cache complete moodboard result."""
        if not self._connected:
            return
        
        try:
            key = self._generate_cache_key("moodboard", image_hash)
            
            # Cache for shorter time since moodboards should feel fresh
            ttl = 3600  # 1 hour
            
            await self.redis_client.setex(
                key,
                ttl,
                json.dumps(moodboard_result)
            )
            
            logger.debug(f"Cached moodboard: {image_hash}")
            
        except Exception as e:
            logger.warning(f"Moodboard cache set error: {str(e)}")
    
    async def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        if not self._connected:
            return {"status": "disconnected"}
        
        try:
            info = await self.redis_client.info()
            
            # Get key counts for different prefixes
            classification_keys = len(await self.redis_client.keys("classification:*"))
            api_keys = len(await self.redis_client.keys("api:*"))
            embedding_keys = len(await self.redis_client.keys("embedding:*"))
            moodboard_keys = len(await self.redis_client.keys("moodboard:*"))
            
            return {
                "status": "connected",
                "memory_used": info.get("used_memory_human", "unknown"),
                "total_keys": info.get("db0", {}).get("keys", 0),
                "cache_breakdown": {
                    "classifications": classification_keys,
                    "api_responses": api_keys,
                    "embeddings": embedding_keys,
                    "moodboards": moodboard_keys
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    async def clear_cache(self, pattern: Optional[str] = None) -> int:
        """Clear cache entries matching pattern."""
        if not self._connected:
            return 0
        
        try:
            if pattern:
                keys = await self.redis_client.keys(pattern)
            else:
                keys = await self.redis_client.keys("*")
            
            if keys:
                deleted = await self.redis_client.delete(*keys)
                logger.info(f"Cleared {deleted} cache entries")
                return deleted
            
            return 0
            
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            return 0
    
    async def close(self):
        """Close Redis connection."""
        if self.redis_client:
            await self.redis_client.close()
            self._connected = False


# Global service instance
cache_service = CacheService()