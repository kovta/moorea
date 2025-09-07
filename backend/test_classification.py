#!/usr/bin/env python3
"""
Test script for aesthetic classification with lifestyle boost.
Usage: python test_classification.py <image_path>
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from services.aesthetic_service import aesthetic_service
from services.clip_service import clip_service
from services.moodboard_service import moodboard_service

# Configure logging to match our backend
import os
log_file = os.path.join(os.path.dirname(__file__), "moodboard_backend.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler(log_file, mode='a')  # File output (append)
    ]
)
logger = logging.getLogger(__name__)


async def test_classification(image_path: str):
    """Test aesthetic classification with lifestyle boost logic."""
    logger.info("🧪 TESTING AESTHETIC CLASSIFICATION")
    logger.info("=" * 50)
    logger.info(f"📸 Image: {image_path}")
    
    try:
        # Initialize services
        logger.info("Initializing services...")
        await aesthetic_service.initialize()
        await clip_service.initialize()
        
        # Load image
        if not os.path.exists(image_path):
            logger.error(f"❌ Image not found: {image_path}")
            return False
            
        with open(image_path, 'rb') as f:
            image_content = f.read()
        
        logger.info(f"✅ Loaded image ({len(image_content)} bytes)")
        
        # Test the classification using the moodboard service logic
        logger.info("🔍 Running aesthetic classification...")
        
        # Get aesthetic vocabulary
        vocabulary = await aesthetic_service.get_vocabulary()
        logger.info(f"📚 Loaded {len(vocabulary)} aesthetic terms")
        
        # Use CLIP for zero-shot classification  
        all_scores = await clip_service.classify_aesthetics(image_content, vocabulary)
        
        # Add descriptions
        for score in all_scores:
            description = await aesthetic_service.get_aesthetic_description(score.name)
            score.description = description
        
        # Log detailed classification results (same as moodboard_service.py)
        logger.info("=== CLIP Classification Results ===")
        for i, score in enumerate(all_scores[:20]):  # Show top 20 to find preppy
            logger.info(f"#{i+1}: {score.name} = {score.score:.3f} ({score.score*100:.1f}%)")
        logger.info("===================================")

        # Focus on the dominant (highest confidence) aesthetic
        dominant_aesthetic = all_scores[0]
        logger.info(f"Selected dominant aesthetic: {dominant_aesthetic.name} ({dominant_aesthetic.score:.3f})")
        
        # Apply intelligent threshold logic (same as moodboard_service.py)
        MINIMUM_CONFIDENCE_THRESHOLD = 0.025  # 2.5% - lowered since lifestyle boost works
        logger.info(f"🏆 HIGHEST CONFIDENCE AESTHETIC: {dominant_aesthetic.name} at {dominant_aesthetic.score:.3f} ({dominant_aesthetic.score*100:.1f}%)")
        
        # Special logic: Prefer lifestyle aesthetics over bridal if they're close
        lifestyle_aesthetics = ["cottagecore", "fairycore", "goblincore", "clean_girl", "soft_girl", "coquette", "vintage", "retro"]
        original_dominant = dominant_aesthetic
        
        for aesthetic in all_scores[:10]:  # Check top 10
            if aesthetic.name in lifestyle_aesthetics and aesthetic.score >= 0.025:  # 2.5% minimum
                boosted_score = aesthetic.score * 6.0  # 600% boost
                logger.info(f"🧮 Lifestyle boost calculation: {aesthetic.name} ({aesthetic.score:.3f} × 6 = {boosted_score:.3f})")
                
                if boosted_score >= dominant_aesthetic.score:  # Give 600% boost to lifestyle aesthetics
                    logger.info(f"🌸 LIFESTYLE BOOST: Promoting '{aesthetic.name}' ({aesthetic.score:.3f}) over '{dominant_aesthetic.name}' ({dominant_aesthetic.score:.3f})")
                    dominant_aesthetic = aesthetic
                    break
        
        # Non-bridal boost: If bridal aesthetic wins, check if non-bridal equivalent is in top 10
        bridal_to_nonbridal = {
            "bridal_minimalist": "minimalist",
            "bridal_modern": "modern", 
            "bridal_vintage": "vintage",
            "bridal_classic": "classic",
            "bridal_romantic": "romantic",
            "bridal_artdeco": "art_deco"
        }
        
        if dominant_aesthetic.name in bridal_to_nonbridal:
            target_aesthetic = bridal_to_nonbridal[dominant_aesthetic.name]
            for aesthetic in all_scores[:10]:  # Check top 10
                if aesthetic.name == target_aesthetic and aesthetic.score >= 0.03:  # 3% minimum
                    boosted_score = aesthetic.score * 4.0  # 400% boost for non-bridal
                    logger.info(f"🚫 NON-BRIDAL BOOST: '{aesthetic.name}' ({aesthetic.score:.3f} × 4 = {boosted_score:.3f}) vs '{dominant_aesthetic.name}' ({dominant_aesthetic.score:.3f})")
                    if boosted_score >= dominant_aesthetic.score:
                        logger.info(f"👔 PROMOTING: '{aesthetic.name}' over bridal variant '{dominant_aesthetic.name}'")
                        dominant_aesthetic = aesthetic
                        break
        
        # Preppy boost: CLIP under-ranks preppy/old_money, check if they're in top 20
        preppy_aesthetics = ["preppy", "old_money", "quiet_luxury"]
        confused_aesthetics = ["mod", "grunge", "maximalist", "streetwear"]  # Aesthetics that often win incorrectly over preppy
        
        if dominant_aesthetic.name in confused_aesthetics:
            for aesthetic in all_scores[:20]:  # Check top 20 for preppy
                if aesthetic.name in preppy_aesthetics and aesthetic.score >= 0.01:  # 1% minimum
                    boosted_score = aesthetic.score * 8.0  # 800% boost for preppy
                    logger.info(f"🎩 PREPPY BOOST: '{aesthetic.name}' ({aesthetic.score:.3f} × 8 = {boosted_score:.3f}) vs '{dominant_aesthetic.name}' ({dominant_aesthetic.score:.3f})")
                    if boosted_score >= dominant_aesthetic.score:
                        logger.info(f"🏌️ PROMOTING: '{aesthetic.name}' over confused aesthetic '{dominant_aesthetic.name}'")
                        dominant_aesthetic = aesthetic
                        break
        
        # Check if aesthetic meets threshold
        if dominant_aesthetic.score < MINIMUM_CONFIDENCE_THRESHOLD:
            logger.warning(f"❌ REJECTED: '{dominant_aesthetic.name}' confidence ({dominant_aesthetic.score:.3f}) below threshold ({MINIMUM_CONFIDENCE_THRESHOLD})")
            logger.info("Falling back to generic 'minimalist' aesthetic for broad inspiration")
            logger.info("🎯 FINAL RESULT: Minimalist Vibes (fallback)")
        else:
            logger.info(f"✅ ACCEPTED: '{dominant_aesthetic.name}' confidence ({dominant_aesthetic.score:.3f}) meets threshold ({MINIMUM_CONFIDENCE_THRESHOLD})")
            
            if dominant_aesthetic != original_dominant:
                logger.info(f"🎯 FINAL RESULT: {dominant_aesthetic.name.title()} Vibes (lifestyle boosted)")
            else:
                logger.info(f"🎯 FINAL RESULT: {dominant_aesthetic.name.title()} Vibes (original)")
        
        logger.info("=" * 50)
        logger.info("✅ Classification test completed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Classification test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Main test runner."""
    if len(sys.argv) != 2:
        print("Usage: python test_classification.py <image_path>")
        print("Example: python test_classification.py /path/to/your/cottagecore_dress.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    success = await test_classification(image_path)
    
    if success:
        print("\n🎉 Test completed successfully! Check the logs above.")
        sys.exit(0)
    else:
        print("\n❌ Test failed. Check the error logs above.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
