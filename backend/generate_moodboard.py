#!/usr/bin/env python3
"""
Full moodboard generation pipeline.
Usage: python generate_moodboard.py <image_path>
"""

import asyncio
import logging
import sys
import time
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from services.aesthetic_service import aesthetic_service
from services.clip_service import clip_service
from services.moodboard_service import moodboard_service
from services.unsplash_client import unsplash_client
from services.pexels_client import pexels_client
from services.flickr_client import flickr_client

# Configure logging
import os
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


async def generate_full_moodboard(image_path: str):
    """Generate a complete moodboard with HTML output."""
    logger.info("🌸 GENERATING COTTAGECORE MOODBOARD")
    logger.info("=" * 60)
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
        
        # 1. AESTHETIC CLASSIFICATION
        logger.info("🔍 Step 1: Aesthetic Classification...")
        vocabulary = await aesthetic_service.get_vocabulary()
        all_scores = await clip_service.classify_aesthetics(image_content, vocabulary)
        
        # Add descriptions
        for score in all_scores:
            description = await aesthetic_service.get_aesthetic_description(score.name)
            score.description = description
        
        # Apply the same logic as our working test
        dominant_aesthetic = all_scores[0]
        MINIMUM_CONFIDENCE_THRESHOLD = 0.025  # 2.5%
        
        # Lifestyle boost logic
        lifestyle_aesthetics = ["cottagecore", "fairycore", "goblincore", "clean_girl", "soft_girl", "coquette", "vintage", "retro"]
        original_dominant = dominant_aesthetic
        
        for aesthetic in all_scores[:10]:
            if aesthetic.name in lifestyle_aesthetics and aesthetic.score >= 0.025:
                boosted_score = aesthetic.score * 6.0
                if boosted_score >= dominant_aesthetic.score:
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
            for aesthetic in all_scores[:10]:
                if aesthetic.name == target_aesthetic and aesthetic.score >= 0.03:
                    boosted_score = aesthetic.score * 4.0
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
        
        if dominant_aesthetic.score < MINIMUM_CONFIDENCE_THRESHOLD:
            logger.warning(f"❌ REJECTED: '{dominant_aesthetic.name}' confidence ({dominant_aesthetic.score:.3f}) below threshold")
            selected_aesthetic = "minimalist"
        else:
            logger.info(f"✅ ACCEPTED: '{dominant_aesthetic.name}' confidence ({dominant_aesthetic.score:.3f})")
            selected_aesthetic = dominant_aesthetic.name
            
        logger.info(f"🎯 SELECTED AESTHETIC: {selected_aesthetic.title()}")
        
        # 2. KEYWORD EXPANSION
        logger.info("🔗 Step 2: Keyword Expansion...")
        primary_keywords = await aesthetic_service.get_keywords_for_aesthetic(selected_aesthetic)
        logger.info(f"📚 Keywords for {selected_aesthetic}: {primary_keywords[:5]}...")
        
        # 3. IMAGE FETCHING
        logger.info("🖼️  Step 3: Fetching Moodboard Images...")
        all_candidates = []
        
        # Use top keywords to fetch images
        search_terms = primary_keywords[:4]  # Top 4 keywords
        
        for keyword in search_terms:
            logger.info(f"🔍 Searching for: '{keyword}'")
            
            # Fetch from multiple sources
            try:
                unsplash_results = await asyncio.wait_for(
                    unsplash_client.search_photos(keyword, per_page=5), timeout=10.0
                )
                all_candidates.extend(unsplash_results[:3])  # Top 3 from Unsplash
                logger.info(f"  📷 Unsplash: {len(unsplash_results)} results")
            except Exception as e:
                logger.warning(f"  ⚠️  Unsplash failed for '{keyword}': {e}")
            
            try:
                pexels_results = await asyncio.wait_for(
                    pexels_client.search_photos(keyword, per_page=5), timeout=10.0
                )
                all_candidates.extend(pexels_results[:2])  # Top 2 from Pexels
                logger.info(f"  📷 Pexels: {len(pexels_results)} results")
            except Exception as e:
                logger.warning(f"  ⚠️  Pexels failed for '{keyword}': {e}")
        
        logger.info(f"🎨 Total images collected: {len(all_candidates)}")
        
        # 4. GENERATE HTML MOODBOARD
        logger.info("🎨 Step 4: Generating HTML Moodboard...")
        
        # Get aesthetic description
        aesthetic_description = await aesthetic_service.get_aesthetic_description(selected_aesthetic)
        
        html_content = generate_html_moodboard(
            selected_aesthetic, 
            aesthetic_description,
            primary_keywords,
            all_candidates,
            image_path
        )
        
        # Save HTML file
        output_filename = f"cottagecore_moodboard_{int(time.time())}.html"
        output_path = f"/Users/kovacstamaspal/dev/moorea/{output_filename}"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info("=" * 60)
        logger.info(f"🎉 SUCCESS! Moodboard generated:")
        logger.info(f"📄 HTML File: {output_path}")
        logger.info(f"🎨 Aesthetic: {selected_aesthetic.title()} Vibes")
        logger.info(f"🖼️  Images: {len(all_candidates)} curated pieces")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Moodboard generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def generate_html_moodboard(aesthetic_name, description, keywords, images, original_image_path):
    """Generate beautiful HTML moodboard."""
    
    # Create image grid HTML
    images_html = ""
    for i, img in enumerate(images):
        # Prefer explicit source_url when available; fall back to pinterest_url
        source_url = getattr(img, 'source_url', None) or getattr(img, 'pinterest_url', None)

        # Photographer attribution (optionally wrapped in anchor)
        if img.photographer:
            if source_url:
                photographer_html = f'<p class="photographer"><a href="{source_url}" target="_blank" rel="noopener noreferrer">Photo by {img.photographer}</a></p>'
            else:
                photographer_html = f'<p class="photographer">Photo by {img.photographer}</p>'
        else:
            photographer_html = ''

        if source_url:
            images_html += f'''
        <div class="image-item">
            <a href="{source_url}" target="_blank" rel="noopener noreferrer">
                <img src="{img.url}" alt="Moodboard inspiration" loading="lazy" onerror="this.style.display='none'">
            </a>
            <div class="image-overlay">
                <p class="image-source">{img.source_api.title()}</p>
                {photographer_html}
            </div>
        </div>
        '''
        else:
            images_html += f'''
        <div class="image-item">
            <img src="{img.url}" alt="Moodboard inspiration" loading="lazy" onerror="this.style.display='none'">
            <div class="image-overlay">
                <p class="image-source">{img.source_api.title()}</p>
                {photographer_html}
            </div>
        </div>
        '''
    
    # Keywords as tags
    keywords_html = ""
    for keyword in keywords[:8]:  # Top 8 keywords
        keywords_html += f'<span class="keyword-tag">#{keyword}</span>'
    
    html_template = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{aesthetic_name.title()} Moodboard - AI Generated</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Georgia', serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            color: #2c3e50;
        }}
        
        .header {{
            text-align: center;
            padding: 3rem 2rem;
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            margin-bottom: 2rem;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            color: #2c3e50;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .header .subtitle {{
            font-size: 1.1rem;
            color: #7f8c8d;
            font-style: italic;
            margin-bottom: 1rem;
        }}
        
        .description {{
            max-width: 600px;
            margin: 0 auto;
            font-size: 1rem;
            line-height: 1.6;
            color: #34495e;
            background: rgba(255, 255, 255, 0.8);
            padding: 1.5rem;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .keywords {{
            text-align: center;
            margin: 2rem 0;
        }}
        
        .keyword-tag {{
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 0.5rem 1rem;
            margin: 0.3rem;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 500;
        }}
        
        .original-image {{
            text-align: center;
            margin: 2rem 0;
        }}
        
        .original-image img {{
            max-width: 300px;
            max-height: 400px;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            object-fit: cover;
        }}
        
        .original-caption {{
            margin-top: 1rem;
            font-style: italic;
            color: #7f8c8d;
        }}
        
        .moodboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .image-item {{
            position: relative;
            overflow: hidden;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            background: white;
        }}
        
        .image-item:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        .image-item img {{
            width: 100%;
            height: 250px;
            object-fit: cover;
            transition: transform 0.3s ease;
        }}
        
        .image-item:hover img {{
            transform: scale(1.05);
        }}
        
        .image-overlay {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(transparent, rgba(0,0,0,0.8));
            color: white;
            padding: 1rem;
            transform: translateY(100%);
            transition: transform 0.3s ease;
        }}
        
        .image-item:hover .image-overlay {{
            transform: translateY(0);
        }}
        
        .image-source {{
            font-size: 0.8rem;
            opacity: 0.9;
            font-weight: 600;
        }}
        
        .photographer {{
            font-size: 0.7rem;
            opacity: 0.7;
            margin-top: 0.3rem;
        }}
        
        .footer {{
            text-align: center;
            padding: 3rem 2rem;
            color: #7f8c8d;
            background: rgba(255, 255, 255, 0.5);
            margin-top: 3rem;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
            }}
            
            .moodboard-grid {{
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 1rem;
                padding: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{aesthetic_name.title()} Vibes</h1>
        <p class="subtitle">AI-Generated Moodboard Inspiration</p>
        <div class="description">
            {description or f"Embrace the {aesthetic_name} aesthetic with this curated collection of inspiring imagery and style elements."}
        </div>
    </div>
    
    <div class="keywords">
        {keywords_html}
    </div>
    
    <div class="original-image">
        <img src="file://{os.path.abspath(original_image_path)}" alt="Your Original Image">
        <p class="original-caption">Your original image, classified as {aesthetic_name}</p>
    </div>
    
    <div class="moodboard-grid">
        {images_html}
    </div>
    
    <div class="footer">
        <p>Generated with AI • {len(images)} curated images • {aesthetic_name.title()} aesthetic</p>
        <p style="margin-top: 0.5rem; font-size: 0.9rem;">
            🌸 Powered by CLIP classification and lifestyle aesthetic boost
        </p>
    </div>
</body>
</html>
    '''
    
    return html_template


async def main():
    """Main moodboard generator."""
    if len(sys.argv) != 2:
        print("Usage: python generate_moodboard.py <image_path>")
        print("Example: python generate_moodboard.py cottagecore2_test.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    success = await generate_full_moodboard(image_path)
    
    if success:
        print("\n🎉 Moodboard generation completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Moodboard generation failed.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
