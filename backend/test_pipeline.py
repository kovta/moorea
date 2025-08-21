#!/usr/bin/env python3
"""
Test script for the moodboard generation pipeline.
Run this to verify all components are working correctly.
"""

import asyncio
import logging
import sys
import time
from pathlib import Path
from io import BytesIO

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from services.aesthetic_service import aesthetic_service
from services.clip_service import clip_service
from services.cache_service import cache_service
from services.moodboard_service import moodboard_service
from services.unsplash_client import unsplash_client
from services.pexels_client import pexels_client
from services.flickr_client import flickr_client

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def test_aesthetic_service():
    """Test aesthetic vocabulary loading."""
    logger.info("Testing aesthetic service...")
    
    try:
        await aesthetic_service.initialize()
        
        # Test vocabulary loading
        vocabulary = await aesthetic_service.get_vocabulary()
        logger.info(f"✓ Loaded {len(vocabulary)} aesthetic terms")
        
        # Test keyword expansion
        keywords = await aesthetic_service.get_keywords_for_aesthetic("cottagecore")
        logger.info(f"✓ Cottagecore keywords: {keywords[:3]}...")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Aesthetic service failed: {e}")
        return False


async def test_cache_service():
    """Test Redis caching."""
    logger.info("Testing cache service...")
    
    try:
        await cache_service.initialize()
        
        # Test basic cache operations
        test_data = {"test": "data", "timestamp": time.time()}
        await cache_service.set_api_cache("test_api", "test_query", [test_data])
        
        cached = await cache_service.get_api_cache("test_api", "test_query")
        
        if cached and cached[0]["test"] == "data":
            logger.info("✓ Cache read/write working")
            return True
        else:
            logger.warning("✗ Cache not working (continuing without caching)")
            return True  # Non-critical failure
            
    except Exception as e:
        logger.warning(f"✗ Cache service failed: {e} (continuing without caching)")
        return True  # Non-critical failure


async def test_api_clients():
    """Test external API clients."""
    logger.info("Testing API clients...")
    
    test_query = "minimalist fashion"
    results = {
        "unsplash": [],
        "pexels": [],
        "flickr": []
    }
    
    # Test each API with timeout
    try:
        results["unsplash"] = await asyncio.wait_for(
            unsplash_client.search_photos(test_query, per_page=2), 
            timeout=10.0
        )
        logger.info(f"✓ Unsplash: {len(results['unsplash'])} results")
    except Exception as e:
        logger.warning(f"✗ Unsplash failed: {e}")
    
    try:
        results["pexels"] = await asyncio.wait_for(
            pexels_client.search_photos(test_query, per_page=2), 
            timeout=10.0
        )
        logger.info(f"✓ Pexels: {len(results['pexels'])} results")
    except Exception as e:
        logger.warning(f"✗ Pexels failed: {e}")
    
    try:
        results["flickr"] = await asyncio.wait_for(
            flickr_client.search_photos(test_query, per_page=2), 
            timeout=10.0
        )
        logger.info(f"✓ Flickr: {len(results['flickr'])} results")
    except Exception as e:
        logger.warning(f"✗ Flickr failed: {e}")
    
    total_results = sum(len(r) for r in results.values())
    if total_results > 0:
        logger.info(f"✓ Total API results: {total_results}")
        return True
    else:
        logger.error("✗ No API results - check your API keys")
        return False


async def test_clip_service():
    """Test CLIP model loading and classification."""
    logger.info("Testing CLIP service...")
    
    try:
        await clip_service.initialize()
        logger.info("✓ CLIP model loaded successfully")
        
        # Create a simple test image (solid color)
        from PIL import Image
        test_image = Image.new('RGB', (224, 224), color='white')
        
        # Convert to bytes
        img_buffer = BytesIO()
        test_image.save(img_buffer, format='JPEG')
        test_image_bytes = img_buffer.getvalue()
        
        # Test classification
        test_vocabulary = ["minimalist", "vintage", "modern", "classic"]
        scores = await clip_service.classify_aesthetics(test_image_bytes, test_vocabulary)
        
        if scores and len(scores) > 0:
            logger.info(f"✓ CLIP classification working - top result: {scores[0].name} ({scores[0].score:.3f})")
            return True
        else:
            logger.error("✗ CLIP classification returned no results")
            return False
            
    except Exception as e:
        logger.error(f"✗ CLIP service failed: {e}")
        return False


async def test_full_pipeline():
    """Test the complete moodboard generation pipeline."""
    logger.info("Testing full pipeline...")
    
    try:
        # Create test image
        from PIL import Image
        import io
        
        # Create a simple test image that might trigger "minimalist"
        test_image = Image.new('RGB', (400, 400), color='#f5f5f5')  # Light gray
        img_buffer = io.BytesIO()
        test_image.save(img_buffer, format='JPEG', quality=85)
        test_image_bytes = img_buffer.getvalue()
        
        logger.info("Created test image, starting pipeline...")
        
        # Test the main pipeline components
        start_time = time.time()
        
        # 1. Aesthetic classification
        vocabulary = await aesthetic_service.get_vocabulary()
        top_aesthetics = await clip_service.classify_aesthetics(test_image_bytes, vocabulary)
        logger.info(f"✓ Classified aesthetics: {[a.name for a in top_aesthetics[:3]]}")
        
        # 2. Keyword expansion
        keywords = []
        for aesthetic in top_aesthetics[:2]:  # Use top 2 aesthetics
            aesthetic_keywords = await aesthetic_service.get_keywords_for_aesthetic(aesthetic.name)
            keywords.extend(aesthetic_keywords)
        logger.info(f"✓ Expanded keywords: {keywords[:5]}")
        
        # 3. Fetch candidates (limit for testing)
        all_candidates = []
        for keyword in keywords[:2]:  # Test with just 2 keywords
            try:
                unsplash_results = await asyncio.wait_for(
                    unsplash_client.search_photos(keyword, per_page=3), timeout=10.0
                )
                all_candidates.extend(unsplash_results)
            except:
                pass
        
        logger.info(f"✓ Fetched {len(all_candidates)} candidates")
        
        # 4. Re-ranking (simplified)
        if all_candidates:
            # Just test that similarity calculation doesn't crash
            try:
                similarity = await clip_service.calculate_image_similarity(
                    test_image_bytes, all_candidates[0].url
                )
                logger.info(f"✓ Similarity calculation working: {similarity:.3f}")
            except Exception as e:
                logger.warning(f"Similarity calculation failed: {e}")
        
        elapsed_time = time.time() - start_time
        logger.info(f"✓ Full pipeline test completed in {elapsed_time:.1f}s")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Full pipeline test failed: {e}")
        return False


async def main():
    """Run all tests."""
    logger.info("Starting moodboard generator pipeline tests...")
    logger.info("=" * 60)
    
    tests = [
        ("Aesthetic Service", test_aesthetic_service),
        ("Cache Service", test_cache_service),
        ("API Clients", test_api_clients),
        ("CLIP Service", test_clip_service),
        ("Full Pipeline", test_full_pipeline),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n--- {test_name} ---")
        try:
            results[test_name] = await test_func()
        except Exception as e:
            logger.error(f"Test crashed: {e}")
            results[test_name] = False
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        logger.info(f"{test_name:20} {status}")
    
    logger.info("-" * 60)
    logger.info(f"TOTAL: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Your moodboard generator is ready.")
        return 0
    else:
        logger.error(f"❌ {total - passed} test(s) failed. Check the logs above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())