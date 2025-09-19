#!/usr/bin/env python3
"""
Quick test to verify dramatic bridal boost logic is working.
This will show you the correct boosted classification percentage.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from services.aesthetic_service import aesthetic_service
from services.clip_service import clip_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_bridal_classification():
    """Test bridal classification with boost logic."""
    
    # Initialize services
    logger.info("🔧 Initializing services...")
    await aesthetic_service.initialize()
    await clip_service.initialize()
    
    # Test with a bridal image
    test_image = "assets/dress.jpg"  # Adjust path as needed
    
    if not Path(test_image).exists():
        logger.error(f"❌ Test image not found: {test_image}")
        return
        
    logger.info(f"📸 Testing classification on: {test_image}")
    
    # Read and classify image
    with open(test_image, "rb") as f:
        image_data = f.read()
    
    # Run CLIP classification
    aesthetics = aesthetic_service.get_all_aesthetics()
    scores = await clip_service.classify_aesthetic(image_data, aesthetics)
    
    # Sort by score
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    logger.info("=== RAW CLIP Results (Before Boost) ===")
    for i, (aesthetic, score) in enumerate(sorted_scores[:10], 1):
        logger.info(f"#{i}: {aesthetic} = {score:.3f} ({score*100:.1f}%)")
    
    # Now apply dramatic bridal boost logic
    logger.info("\n=== APPLYING DRAMATIC BRIDAL BOOST ===")
    
    dramatic_bridal_aesthetics = {
        "bridal_ballgown", "bridal_princess", "bridal_mermaid", 
        "bridal_romantic", "bridal_artdeco"
    }
    
    best_aesthetic = sorted_scores[0][0]  # Dominant aesthetic
    best_score = sorted_scores[0][1]
    
    # Check for dramatic bridal boost
    for aesthetic, score in sorted_scores[:10]:
        if aesthetic in dramatic_bridal_aesthetics and score >= 0.02:
            boosted_score = score * 5.0
            if boosted_score > best_score:
                logger.info(f"⚡ DRAMATIC BRIDAL BOOST: {aesthetic}")
                logger.info(f"   Original: {score:.3f} ({score*100:.1f}%)")
                logger.info(f"   Boosted:  {boosted_score:.3f} ({boosted_score*100:.1f}%)")
                best_aesthetic = aesthetic
                best_score = boosted_score
                break
    
    logger.info(f"\n🎯 FINAL RESULT: {best_aesthetic} ({best_score*100:.1f}% confidence)")

if __name__ == "__main__":
    asyncio.run(test_bridal_classification())
