"""Moodboard generation service - orchestrates the full pipeline."""

import asyncio
import logging
from datetime import datetime
from typing import List
from uuid import UUID

from config import settings
from models import JobStatus, MoodboardResult, AestheticScore, ImageCandidate
from services.job_service import job_service
from services.unsplash_client import unsplash_client
from services.pexels_client import pexels_client
from services.flickr_client import flickr_client
from services.pinterest_client import pinterest_client
"""
NOTE: clip_service and aesthetic_service import heavy ML dependencies (torch/CLIP).
To allow local runs without ML packages, these services are imported lazily inside
methods and guarded with fallbacks. This prevents ImportError at module import time
so that moodboard routes can be enabled without ML installed.
"""

logger = logging.getLogger(__name__)


class MoodboardService:
    """Service for orchestrating moodboard generation pipeline."""
    
    def __init__(self):
        # Pinterest client is now OAuth-based and initialized globally
        pass
    
    async def queue_generation(self, job_id: UUID, image_content: bytes, pinterest_consent: bool = False) -> None:
        """Queue moodboard generation job."""
        # For now, process immediately (add proper queue later)
        asyncio.create_task(self._process_moodboard(job_id, image_content, pinterest_consent))
    
    async def _process_moodboard(self, job_id: UUID, image_content: bytes, pinterest_consent: bool = False) -> None:
        """Process moodboard generation pipeline."""
        try:
            await job_service.update_job_status(job_id, JobStatus.PROCESSING, progress=0)
            
            # Step 1: CLIP Classification (placeholder)
            logger.info(f"Starting aesthetic classification for job {job_id}")
            await asyncio.sleep(1)  # Simulate processing
            top_aesthetics = await self._classify_aesthetics(image_content)
            await job_service.update_job_status(job_id, JobStatus.PROCESSING, progress=25)
            
            # Step 2: Keyword expansion with intelligent filtering
            logger.info(f"Expanding keywords for job {job_id}")
            search_keywords, negative_keywords = await self._expand_keywords(top_aesthetics)
            logger.info(f"Generated {len(search_keywords)} search keywords, avoiding {len(negative_keywords)} negative terms")
            await job_service.update_job_status(job_id, JobStatus.PROCESSING, progress=50)
            
            # Step 3: Fetch candidates (placeholder)
            logger.info(f"Fetching image candidates for job {job_id}")
            candidates = await self._fetch_candidates(search_keywords, pinterest_consent)
            await job_service.update_job_status(job_id, JobStatus.PROCESSING, progress=75)
            
            # Step 4: Re-rank and select (placeholder)
            logger.info(f"Re-ranking candidates for job {job_id}")
            final_images = await self._rerank_candidates(image_content, candidates)
            await job_service.update_job_status(job_id, JobStatus.PROCESSING, progress=100)
            
            # Store result
            logger.info(f"📦 Storing moodboard result for job {job_id}")
            logger.info(f"   Top aesthetics: {[a.name for a in top_aesthetics]}")
            logger.info(f"   Final images count: {len(final_images)}")
            
            result = MoodboardResult(
                job_id=job_id,
                status=JobStatus.COMPLETED,
                top_aesthetics=top_aesthetics,
                images=final_images,
                created_at=datetime.now(),
                processing_time=5.0  # placeholder
            )
            
            await job_service.store_job_result(job_id, result)
            logger.info(f"✅ Completed moodboard generation for job {job_id} with {len(final_images)} images")
            
            if len(final_images) == 0:
                logger.error(f"❌ WARNING: Moodboard result has 0 images! This will only show the uploaded image.")
            
        except Exception as e:
            logger.error(f"Error processing moodboard for job {job_id}: {str(e)}")
            await job_service.update_job_status(
                job_id, 
                JobStatus.FAILED, 
                error_message=str(e)
            )
    
    async def _classify_aesthetics(self, image_content: bytes) -> List[AestheticScore]:
        """Classify image aesthetics using CLIP with confidence threshold."""
        try:
            # Lazy import aesthetic_service to avoid hard dependency at module load
            try:
                from services.aesthetic_service import aesthetic_service
            except Exception as e:
                logger.warning(f"Aesthetic service unavailable, using fallback: {e}")
                return [
                    AestheticScore(
                        name="minimalist",
                        score=0.60,
                        description="Clean, simple, functional design"
                    )
                ]

            # Get aesthetic vocabulary
            vocabulary = await aesthetic_service.get_vocabulary()
            
            # Lazy import CLIP service (heavy ML deps)
            try:
                from services.clip_service import clip_service
            except Exception as e:
                logger.warning(f"CLIP service unavailable, using fallback: {e}")
                return [
                    AestheticScore(
                        name="minimalist",
                        score=0.60,
                        description="Clean, simple, functional design"
                    )
                ]

            # Use CLIP for zero-shot classification
            all_scores = await clip_service.classify_aesthetics(image_content, vocabulary)
            
            # Add descriptions from aesthetic service
            for score in all_scores:
                description = await aesthetic_service.get_aesthetic_description(score.name)
                score.description = description
            
            # Log detailed classification results
            logger.info("=== CLIP Classification Results ===")
            for i, score in enumerate(all_scores[:20]):  # Show top 20 to catch more specific aesthetics
                logger.info(f"#{i+1}: {score.name} = {score.score:.3f} ({score.score*100:.1f}%)")
            
            # Check specifically for mob_wife and dark_academia even if not in top 20
            mob_wife_score = next((score for score in all_scores if score.name == "mob_wife"), None)
            if mob_wife_score:
                logger.info(f"🔍 MOB_WIFE FOUND: #{all_scores.index(mob_wife_score)+1} = {mob_wife_score.score:.3f} ({mob_wife_score.score*100:.1f}%)")
            else:
                logger.info("❌ MOB_WIFE NOT FOUND in classification results")
            
            dark_academia_score = next((score for score in all_scores if score.name == "dark_academia"), None)
            if dark_academia_score:
                logger.info(f"🔍 DARK_ACADEMIA FOUND: #{all_scores.index(dark_academia_score)+1} = {dark_academia_score.score:.3f} ({dark_academia_score.score*100:.1f}%)")
            else:
                logger.info("❌ DARK_ACADEMIA NOT FOUND in classification results")
            
            light_academia_score = next((score for score in all_scores if score.name == "light_academia"), None)
            if light_academia_score:
                logger.info(f"🔍 LIGHT_ACADEMIA FOUND: #{all_scores.index(light_academia_score)+1} = {light_academia_score.score:.3f} ({light_academia_score.score*100:.1f}%)")
            else:
                logger.info("❌ LIGHT_ACADEMIA NOT FOUND in classification results")
            
            maximalist_score = next((score for score in all_scores if score.name == "maximalist"), None)
            if maximalist_score:
                logger.info(f"🔍 MAXIMALIST FOUND: #{all_scores.index(maximalist_score)+1} = {maximalist_score.score:.3f} ({maximalist_score.score*100:.1f}%)")
            else:
                logger.info("❌ MAXIMALIST NOT FOUND in classification results")
            
            gorpcore_score = next((score for score in all_scores if score.name == "gorpcore"), None)
            if gorpcore_score:
                logger.info(f"🔍 GORPCORE FOUND: #{all_scores.index(gorpcore_score)+1} = {gorpcore_score.score:.3f} ({gorpcore_score.score*100:.1f}%)")
            else:
                logger.info("❌ GORPCORE NOT FOUND in classification results")
            logger.info("===================================")

            # Focus on the dominant (highest confidence) aesthetic
            dominant_aesthetic = all_scores[0]
            logger.info(f"Selected dominant aesthetic: {dominant_aesthetic.name} ({dominant_aesthetic.score:.3f})")
            
            # Apply intelligent threshold logic
            MINIMUM_CONFIDENCE_THRESHOLD = 0.01  # 1% - lowered to catch more specific aesthetics like mob_wife
            logger.info(f"🏆 HIGHEST CONFIDENCE AESTHETIC: {dominant_aesthetic.name} at {dominant_aesthetic.score:.3f} ({dominant_aesthetic.score*100:.1f}%)")
            
            # ⚡ SYSTEMATIC CONFIDENCE-BASED BOOST LOGIC
            # Define aesthetic categories for targeted boosting
            lifestyle_aesthetics = {"cottagecore", "fairycore", "goblincore", "clean_girl", "soft_girl", "coquette", "vintage", "retro", "coastal_grandmother", "gorpcore"}
            preppy_aesthetics = {"preppy", "old_money", "quiet_luxury", "the_row"}
            luxury_aesthetics = {"mob_wife", "office_siren", "barbiecore", "maximalist_luxury", "quiet_luxury"}
            academic_aesthetics = {"dark_academia", "light_academia", "romantic_academia"}
            dramatic_bridal_aesthetics = {"bridal_ballgown", "bridal_princess", "bridal_mermaid", "bridal_romantic", "bridal_artdeco"}
            
            best_aesthetic = dominant_aesthetic
            best_score = dominant_aesthetic.score
            
            def calculate_boost(score: float, category: str) -> float:
                """Calculate boost multiplier based on confidence level and category."""
                if score >= 0.15:  # Very high confidence - no boost needed
                    return 1.0
                elif score >= 0.08:  # High confidence - tiny boost
                    return 1.2
                elif score >= 0.05:  # Medium-high confidence - small boost
                    return 1.5
                elif score >= 0.02:  # Medium confidence - moderate boost
                    return 2.5
                elif score >= 0.01:  # Low confidence - high boost
                    return 4.0
                elif score >= 0.005:  # Very low confidence - very high boost
                    return 8.0
                else:  # Extremely low confidence - maximum boost
                    return 15.0
            
            # Apply systematic boosts to ALL aesthetics (not just top 20)
            logger.info(f"🔍 Checking {len(all_scores)} aesthetics for boosts...")
            for aesthetic in all_scores:
                boost_multiplier = 1.0
                category = "general"
                
                # Determine category and boost
                if aesthetic.name in lifestyle_aesthetics:
                    # Lifestyle aesthetics get extra boost for competitiveness
                    base_boost = calculate_boost(aesthetic.score, "lifestyle")
                    boost_multiplier = base_boost * 3.0  # Extra 200% boost for lifestyle
                    category = "lifestyle"
                    if aesthetic.name == "gorpcore":
                        logger.info(f"🎯 GORPCORE BOOST CALCULATION: {aesthetic.score:.3f} × {boost_multiplier:.1f} = {aesthetic.score * boost_multiplier:.3f}")
                elif aesthetic.name in preppy_aesthetics:
                    boost_multiplier = calculate_boost(aesthetic.score, "preppy")
                    category = "preppy"
                elif aesthetic.name in luxury_aesthetics:
                    boost_multiplier = calculate_boost(aesthetic.score, "luxury")
                    category = "luxury"
                elif aesthetic.name in academic_aesthetics:
                    boost_multiplier = calculate_boost(aesthetic.score, "academic")
                    category = "academic"
                elif aesthetic.name in dramatic_bridal_aesthetics:
                    # FIXED: Only boost bridal if confidence is reasonably high (>= 0.08 or 8%)
                    # This prevents swimsuits and other white clothing from being misclassified
                    if aesthetic.score >= 0.08:  # Require minimum 8% confidence for bridal
                        boost_multiplier = calculate_boost(aesthetic.score, "bridal")
                        category = "bridal"
                        logger.info(f"💍 BRIDAL BOOST: {aesthetic.name} ({aesthetic.score:.3f}) meets threshold")
                    else:
                        # Skip bridal boost if confidence is too low
                        boost_multiplier = 1.0
                        logger.info(f"🚫 BRIDAL REJECTED: {aesthetic.name} ({aesthetic.score:.3f}) below 8% threshold")
                elif aesthetic.name == "maximalist":
                    boost_multiplier = calculate_boost(aesthetic.score, "maximalist")
                    category = "maximalist"
                elif aesthetic.name == "gorpcore":
                    # FIXED: Reduce massive boost and add context validation
                    # Only apply gorpcore boost if image actually contains outdoor/hiking elements
                    if await self._validate_gorpcore_context(image_content, aesthetic.name):
                        boost_multiplier = 3.0  # Reduced from 50x to 3x boost
                        category = "gorpcore"
                        logger.info(f"🏔️ GORPCORE VALIDATED: {aesthetic.name} context confirmed, applying 3x boost")
                    else:
                        # Skip gorpcore boost if context doesn't match
                        boost_multiplier = 1.0
                        logger.info(f"🚫 GORPCORE REJECTED: {aesthetic.name} context doesn't match outdoor/hiking elements")
                
                # Apply boost if it improves the score
                if boost_multiplier > 1.0:
                    boosted = aesthetic.score * boost_multiplier
                    if boosted > best_score:
                        logger.info(f"⚡ {category.upper()}: {aesthetic.name} ({aesthetic.score:.3f} × {boost_multiplier} = {boosted:.3f})")
                        best_aesthetic, best_score = aesthetic, boosted
            
            # All aesthetics are now checked above, no need for special checks
            
            dominant_aesthetic = best_aesthetic
            
            # Update the aesthetic score to reflect the boosted confidence
            # Cap at 1.0 to prevent >100% display in frontend
            capped_score = min(best_score, 1.0)
            dominant_aesthetic.score = capped_score
            
            # Use boosted score for threshold check, not original score
            effective_score = best_score  # This is the boosted score
            if effective_score < MINIMUM_CONFIDENCE_THRESHOLD:
                logger.warning(f"❌ REJECTED: '{dominant_aesthetic.name}' effective confidence ({effective_score:.3f}) below threshold ({MINIMUM_CONFIDENCE_THRESHOLD})")
                logger.info("Falling back to generic 'minimalist' aesthetic for broad inspiration")
                fallback_aesthetic = AestheticScore(name="minimalist", score=0.65, description="Clean, versatile style that works with many pieces")
                return [fallback_aesthetic]
            
            logger.info(f"✅ ACCEPTED: '{dominant_aesthetic.name}' effective confidence ({effective_score:.3f}) meets threshold ({MINIMUM_CONFIDENCE_THRESHOLD})")
            
            # POST-PROCESSING FILTER: Fix common misclassifications AFTER boosts
            all_scores = await self._apply_classification_filters(image_content, all_scores)
            
            # Re-select dominant aesthetic after filtering
            dominant_aesthetic = all_scores[0] if all_scores else dominant_aesthetic
            
            # Include dominant + up to 2 supporting aesthetics (if they meet a lower bar)
            result_aesthetics = [dominant_aesthetic]
            for aesthetic in all_scores[1:3]:  # Check next 2 aesthetics
                if aesthetic.score >= 0.35:  # Lower threshold for supporting aesthetics
                    result_aesthetics.append(aesthetic)
                    logger.info(f"➕ SUPPORTING: '{aesthetic.name}' at {aesthetic.score:.3f}")
            
            return result_aesthetics
            
        except Exception as e:
            logger.error(f"Error in aesthetic classification: {str(e)}")
            # Fallback to mock data if CLIP fails
            return [
                AestheticScore(
                    name="minimalist",
                    score=0.60,
                    description="Clean, simple, functional design"
                )
            ]
    
    async def _expand_keywords(self, aesthetics: List[AestheticScore]) -> tuple[List[str], List[str]]:
        """Expand aesthetics to search keywords with intelligent filtering."""
        keywords = []
        negative_keywords = set()

        # Lazy import aesthetic_service; fallback to generic keywords when unavailable
        aesthetic_service_available = True
        try:
            from services.aesthetic_service import aesthetic_service
        except Exception as e:
            aesthetic_service_available = False
            logger.warning(f"Aesthetic service unavailable during keyword expansion, using fallback keywords: {e}")

        for aesthetic in aesthetics:
            if aesthetic_service_available:
                try:
                    # Get positive keywords
                    aesthetic_keywords = await aesthetic_service.get_keywords_for_aesthetic(aesthetic.name)
                    keywords.extend(aesthetic_keywords)

                    # Get negative keywords to avoid
                    aesthetic_negatives = await aesthetic_service.get_negative_keywords_for_aesthetic(aesthetic.name)
                    negative_keywords.update(aesthetic_negatives)

                    # Get color palette for intelligent filtering
                    color_palette = await aesthetic_service.get_color_palette_for_aesthetic(aesthetic.name)
                    if color_palette:
                        logger.info(f"Using color palette for {aesthetic.name}: {color_palette}")
                except Exception as ex:
                    logger.warning(f"Error using aesthetic service for '{aesthetic.name}', falling back: {ex}")
                    # Fallback generic keywords for the aesthetic name
                    name = aesthetic.name.replace('_', ' ')
                    keywords.extend([f"{name} outfit", f"{name} fashion", f"{name} style"])
            else:
                # Fallback generic keywords when service unavailable
                name = aesthetic.name.replace('_', ' ')
                keywords.extend([f"{name} outfit", f"{name} fashion", f"{name} style"])

        # If still no keywords, add minimalist fallbacks
        if not keywords:
            keywords = ["minimalist outfit", "clean fashion", "neutral wardrobe"]

        # Remove duplicates and apply negative filtering
        unique_keywords = []
        for keyword in keywords:
            if not any(neg in keyword.lower() for neg in negative_keywords):
                unique_keywords.append(keyword)

        return unique_keywords, list(negative_keywords)
    
    async def _fetch_candidates(self, keywords: List[str], pinterest_consent: bool = False) -> List[ImageCandidate]:
        """Fetch image candidates from APIs - optimized for speed."""
        all_candidates = []
        
        # ⚡ SPEED OPTIMIZATION: Fewer keywords, fewer images, faster timeout
        top_keywords = keywords[:3]  # Reduced to 3 keywords for speed
        images_per_keyword = max(2, settings.max_candidates // len(top_keywords)) if top_keywords else 4
        
        logger.info(f"🔍 Fetching images for keywords: {top_keywords}")
        logger.info(f"   Images per keyword: {images_per_keyword}")
        logger.info(f"   Unsplash API key configured: {bool(settings.unsplash_access_key)}")
        logger.info(f"   Pexels API key configured: {bool(settings.pexels_api_key)}; enabled: {getattr(settings, 'enable_pexels', True)}")
        logger.info(f"   Pinterest consent: {pinterest_consent}")
        
        # ⚡ Use multiple APIs with fallback: Unsplash → Pexels → Pinterest
        all_tasks = []
        for keyword in top_keywords:
            tasks = []
            
            # Always try Unsplash first
            if settings.unsplash_access_key:
                tasks.append(unsplash_client.search_photos(keyword, per_page=images_per_keyword))
            else:
                logger.warning(f"⚠️ Unsplash API key not configured, skipping Unsplash for '{keyword}'")
            
            # Try Pexels as fallback
            if settings.pexels_api_key and getattr(settings, 'enable_pexels', True):
                tasks.append(pexels_client.search_photos(keyword, per_page=images_per_keyword))
            else:
                logger.warning(f"⚠️ Pexels disabled or API key not configured, skipping Pexels for '{keyword}'")
            
            # Add Pinterest if API key is configured or user consented with OAuth
            if await pinterest_client.is_authenticated():
                logger.info(f"   📌 Including Pinterest for '{keyword}'")
                tasks.append(pinterest_client.search_and_extract_images(keyword, max_images=images_per_keyword))
            elif pinterest_consent:
                logger.warning(f"   ⚠️ Pinterest consent given but API not authenticated for '{keyword}'")
            
            all_tasks.extend(tasks)
        
        # Execute all API calls concurrently with shorter timeout
        api_count = sum([
            bool(settings.unsplash_access_key),
            bool(settings.pexels_api_key and getattr(settings, 'enable_pexels', True)),
            bool(pinterest_consent and await pinterest_client.is_authenticated())
        ])
        logger.info(f"⚡ SPEED MODE: Fetching from {api_count} API(s) for {len(top_keywords)} keywords ({len(all_tasks)} total requests)")
        
        if not all_tasks:
            logger.error("❌ No API keys configured! Falling back to local images in backend/images.")
            return await self._local_folder_candidates()
        
        try:
            # Use asyncio.wait_for with shorter timeout for speed
            results = await asyncio.wait_for(
                asyncio.gather(*all_tasks, return_exceptions=True),
                timeout=8.0  # Allow a bit more time for provider responses
            )
            
            successful_count = 0
            failed_count = 0
            for i, result in enumerate(results):
                if isinstance(result, list):  # Successful result
                    all_candidates.extend(result)
                    successful_count += 1
                    logger.info(f"✅ API call {i+1} succeeded: {len(result)} images")
                elif isinstance(result, Exception):
                    failed_count += 1
                    logger.warning(f"❌ API call {i+1} failed: {type(result).__name__}: {result}")
                else:
                    failed_count += 1
                    logger.warning(f"❌ API call {i+1} returned unexpected type: {type(result)}")
            
            logger.info(f"📊 API Results: {successful_count} succeeded, {failed_count} failed, {len(all_candidates)} total images fetched")
                    
        except asyncio.TimeoutError:
            logger.warning("⚠️ API calls timed out after 5 seconds, using partial results")
        
        # Remove duplicates by URL and limit total
        seen_urls = set()
        unique_candidates = []
        for candidate in all_candidates:
            if candidate.url not in seen_urls:
                seen_urls.add(candidate.url)
                unique_candidates.append(candidate)
                if len(unique_candidates) >= settings.max_candidates:
                    break
        
        logger.info(f"⚡ Fast fetch: {len(unique_candidates)} unique candidates (target: {settings.max_candidates})")

        # Fallback: if no candidates found, try generic keywords via Unsplash only
        if not unique_candidates:
            logger.warning("⚠️ No candidates from primary keywords. Trying generic fallback keywords via Unsplash...")
            fallback_keywords = ["minimalist outfit", "vintage fashion", "cottagecore dress"]
            for kw in fallback_keywords:
                try:
                    res = await unsplash_client.search_photos(kw, per_page=4)
                    for candidate in res:
                        if candidate.url not in seen_urls:
                            seen_urls.add(candidate.url)
                            unique_candidates.append(candidate)
                            if len(unique_candidates) >= settings.max_candidates:
                                break
                    logger.info(f"  Fallback '{kw}': {len(res)} images; total unique now {len(unique_candidates)}")
                except Exception as ex:
                    logger.warning(f"  Fallback Unsplash error for '{kw}': {ex}")

        # Final fallback: local folder images served via /static
        if not unique_candidates:
            logger.warning("⚠️ Still no candidates; using local folder images.")
            unique_candidates = await self._local_folder_candidates()

        if not unique_candidates:
            logger.error("❌ No image candidates found! Check API keys and network connectivity.")

        return unique_candidates

    async def _local_folder_candidates(self) -> List[ImageCandidate]:
        """Build candidates from local backend/images folder and serve via /static."""
        try:
            from pathlib import Path
            backend_dir = Path(__file__).parent.parent
            images_dir = backend_dir / "images"
            if not images_dir.exists():
                logger.error(f"Local images directory not found: {images_dir}")
                return []
            exts = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
            files = [p for p in images_dir.iterdir() if p.is_file() and p.suffix.lower() in exts]
            files = files[:settings.final_moodboard_size]
            base = settings.backend_url.rstrip("/")
            candidates: List[ImageCandidate] = []
            for f in files:
                url = f"{base}/static/{f.name}"
                candidates.append(ImageCandidate(
                    id=f"local_{f.name}",
                    url=url,
                    thumbnail_url=url,
                    photographer=None,
                    source_api="local",
                    source_url=url
                ))
            logger.info(f"Local folder candidates: {len(candidates)} images from {images_dir}")
            return candidates
        except Exception as e:
            logger.error(f"Local folder candidates error: {e}")
            return []
    
    async def _rerank_candidates(self, original_image: bytes, 
                                candidates: List[ImageCandidate]) -> List[ImageCandidate]:
        """Re-rank candidates using CLIP similarity."""
        try:
            if not candidates:
                logger.warning("⚠️ No candidates to rerank!")
                return []
            
            logger.info(f"🔄 Re-ranking {len(candidates)} candidates using CLIP similarity")
            
            # Lazy import CLIP service to avoid hard dependency at import time
            try:
                from services.clip_service import clip_service
            except Exception as e:
                logger.warning(f"CLIP service unavailable, returning top candidates without scoring: {e}")
                return candidates[:settings.final_moodboard_size]

            # Get original image embedding
            original_embedding = await clip_service.get_image_embedding(original_image)
            logger.info(f"✅ Got original image embedding")
            
            # Calculate similarities for all candidates
            candidate_urls = [c.url for c in candidates]
            logger.info(f"📊 Calculating similarity for {len(candidate_urls)} candidate URLs")
            similarities = await clip_service.batch_similarity(original_embedding, candidate_urls)
            logger.info(f"✅ Got {len(similarities)} similarity scores")
            
            # Add similarity scores and sort by score
            scored_candidates = []
            for candidate, similarity in zip(candidates, similarities):
                candidate.similarity_score = similarity
                scored_candidates.append(candidate)
            
            # Log similarity score distribution
            if scored_candidates:
                scores = [c.similarity_score or 0 for c in scored_candidates]
                logger.info(f"📊 Similarity scores - Min: {min(scores):.3f}, Max: {max(scores):.3f}, Avg: {sum(scores)/len(scores):.3f}")
                logger.info(f"   Top 5 scores: {sorted(scores, reverse=True)[:5]}")
            
            # Sort by similarity score (highest first)
            scored_candidates.sort(key=lambda x: x.similarity_score or 0, reverse=True)
            
            # Filter by minimum similarity threshold (lowered to 15% to be more inclusive)
            MIN_SIMILARITY_THRESHOLD = 0.15
            filtered_candidates = [
                candidate for candidate in scored_candidates 
                if (candidate.similarity_score or 0) >= MIN_SIMILARITY_THRESHOLD
            ]
            
            logger.info(f"📊 Filtered {len(scored_candidates)} candidates to {len(filtered_candidates)} above {MIN_SIMILARITY_THRESHOLD} similarity")
            
            # Return filtered candidates (up to final moodboard size)
            if len(filtered_candidates) >= 3:  # Need at least 3 good matches
                final_count = min(len(filtered_candidates), settings.final_moodboard_size)
                logger.info(f"✅ Returning {final_count} filtered candidates")
                return filtered_candidates[:final_count]
            else:
                # Fallback: if too few high-quality matches, lower threshold to 10%
                logger.warning(f"⚠️ Only {len(filtered_candidates)} high-quality matches, using 10% threshold")
                fallback_candidates = [
                    candidate for candidate in scored_candidates 
                    if (candidate.similarity_score or 0) >= 0.10
                ]
                if len(fallback_candidates) >= 3:
                    final_count = min(len(fallback_candidates), settings.final_moodboard_size)
                    logger.info(f"✅ Returning {final_count} fallback candidates (10% threshold)")
                    return fallback_candidates[:final_count]
                else:
                    # Final fallback: return top candidates regardless of similarity
                    logger.warning(f"⚠️ Very few matches even at 10%, returning top {settings.final_moodboard_size} candidates")
                    final_count = min(len(scored_candidates), settings.final_moodboard_size)
                    return scored_candidates[:final_count]
            
        except Exception as e:
            logger.error(f"❌ Error in candidate re-ranking: {str(e)}")
            logger.error(f"   Exception type: {type(e).__name__}")
            import traceback
            logger.error(f"   Traceback: {traceback.format_exc()}")
            # Fallback: return first N candidates without scoring
            logger.warning(f"⚠️ Returning {min(len(candidates), settings.final_moodboard_size)} candidates without similarity scoring")
            return candidates[:settings.final_moodboard_size]

    async def _apply_classification_filters(self, image_content: bytes, all_scores: List[AestheticScore]) -> List[AestheticScore]:
        """Apply post-processing filters to fix common misclassifications - optimized for speed."""
        try:
            # Lazy import clip_service; if unavailable, skip filters
            try:
                from services.clip_service import clip_service
            except Exception as e:
                logger.warning(f"CLIP service unavailable during post-filters, skipping filters: {e}")
                return all_scores
            # SPEED OPTIMIZATION: Only apply filters if problematic aesthetics are in top 5
            top_aesthetics = [score.name for score in all_scores[:5]]
            
            if "mod" in top_aesthetics or "gorpcore" in top_aesthetics:
                # Filter 1: Fix boot misclassifications (only if needed)
                boot_keywords = ["boots", "knee high boots", "riding boots"]  # Removed cowboy boots
                boot_scores = await clip_service.classify_aesthetics(image_content, boot_keywords)
                max_boot_score = max([score.score for score in boot_scores]) if boot_scores else 0
                
                # Check if it's specifically cowboy boots by looking for western elements
                western_keywords = ["cowboy boots", "western wear", "ranch style", "country fashion", "rural lifestyle"]
                western_scores = await clip_service.classify_aesthetics(image_content, western_keywords)
                max_western_score = max([score.score for score in western_scores]) if western_scores else 0
                is_cowboy_boots = max_western_score > 0.25  # 25% confidence threshold for western elements
                
                if max_boot_score > 0.3:  # 30% confidence threshold for boots
                    logger.info(f"🔧 BOOT DETECTED: {max_boot_score:.3f} confidence")
                    
                    if is_cowboy_boots:
                        # Special handling for cowboy boots - boost farmcore
                        farmcore_score = next((score for score in all_scores if score.name == "farmcore"), None)
                        if farmcore_score:
                            farmcore_score.score *= 3.0  # Increased boost for farmcore
                            logger.info(f"🤠 COWBOY BOOT FILTER: Boosted farmcore score to {farmcore_score.score:.3f} (western score: {max_western_score:.3f})")
                    else:
                        # Regular boot handling for non-cowboy boots
                        # Fix mod misclassification
                        mod_score = next((score for score in all_scores if score.name == "mod"), None)
                        if mod_score and mod_score.score > 0.1:
                            mod_score.score *= 0.2  # Reduce mod by 80%
                            logger.info(f"🔧 BOOT FILTER: Reduced mod score to {mod_score.score:.3f}")
                        
                        # Fix gorpcore misclassification
                        gorpcore_score = next((score for score in all_scores if score.name == "gorpcore"), None)
                        if gorpcore_score and gorpcore_score.score > 0.1:
                            gorpcore_score.score *= 0.1  # Reduce gorpcore by 90%
                            logger.info(f"🔧 BOOT FILTER: Reduced gorpcore score to {gorpcore_score.score:.3f}")
                        
                        # Boost more appropriate aesthetics for boots
                        vintage_score = next((score for score in all_scores if score.name == "vintage"), None)
                        preppy_score = next((score for score in all_scores if score.name == "preppy"), None)
                        old_money_score = next((score for score in all_scores if score.name == "old_money"), None)
                        
                        if vintage_score:
                            vintage_score.score *= 2.0  # Boost vintage for boots
                            logger.info(f"🔧 BOOT FILTER: Boosted vintage score to {vintage_score.score:.3f}")
                        if preppy_score:
                            preppy_score.score *= 1.8  # Boost preppy for boots
                            logger.info(f"🔧 BOOT FILTER: Boosted preppy score to {preppy_score.score:.3f}")
                        if old_money_score:
                            old_money_score.score *= 1.6  # Boost old money for boots
                            logger.info(f"🔧 BOOT FILTER: Boosted old_money score to {old_money_score.score:.3f}")
            
            # Filter 2: Fix cozy sweater misclassification (quiet_luxury vs hygge/cozycore)
            if "quiet_luxury" in top_aesthetics:
                cozy_sweater_keywords = ["patterned sweater", "knit sweater", "cozy sweater", "warm knitwear", "comfortable sweater", "soft textures"]
                cozy_sweater_scores = await clip_service.classify_aesthetics(image_content, cozy_sweater_keywords)
                max_cozy_score = max([score.score for score in cozy_sweater_scores]) if cozy_sweater_scores else 0
                
                if max_cozy_score > 0.25:  # 25% confidence threshold for cozy sweater elements
                    logger.info(f"🧶 COZY SWEATER DETECTED: {max_cozy_score:.3f} confidence")
                    
                    # Reduce quiet_luxury score for cozy/patterned items
                    quiet_luxury_score = next((score for score in all_scores if score.name == "quiet_luxury"), None)
                    if quiet_luxury_score and quiet_luxury_score.score > 0.1:
                        quiet_luxury_score.score *= 0.3  # Reduce quiet_luxury by 70%
                        logger.info(f"🔧 COZY SWEATER FILTER: Reduced quiet_luxury score to {quiet_luxury_score.score:.3f}")
                    
                    # Boost hygge and cozycore for cozy sweaters
                    hygge_score = next((score for score in all_scores if score.name == "hygge"), None)
                    cozycore_score = next((score for score in all_scores if score.name == "cozycore"), None)
                    
                    if hygge_score:
                        hygge_score.score *= 2.5  # Boost hygge for cozy sweaters
                        logger.info(f"🔧 COZY SWEATER FILTER: Boosted hygge score to {hygge_score.score:.3f}")
                    if cozycore_score:
                        cozycore_score.score *= 2.5  # Boost cozycore for cozy sweaters
                        logger.info(f"🔧 COZY SWEATER FILTER: Boosted cozycore score to {cozycore_score.score:.3f}")
            
            # Re-sort scores after filtering
            all_scores.sort(key=lambda x: x.score, reverse=True)
            
            return all_scores
            
        except Exception as e:
            logger.error(f"Error in classification filters: {str(e)}")
            return all_scores

    async def _validate_gorpcore_context(self, image_content: bytes, aesthetic_name: str) -> bool:
        """Validate if image actually contains outdoor/hiking elements before applying gorpcore boost."""
        try:
            # Define outdoor/hiking elements that should trigger gorpcore
            outdoor_keywords = [
                "hiking gear", "outdoor equipment", "technical clothing", "waterproof jacket", 
                "cargo pants", "utility vest", "hiking backpack", "outdoor adventure", 
                "mountain gear", "trail hiking", "outdoor activity", "hiking trail"
            ]
            
            # Define non-outdoor elements that should NOT trigger gorpcore
            non_outdoor_keywords = [
                "formal boots", "dress boots", "fashion boots", "knee high boots", 
                "riding boots", "leather boots", "casual boots", "street boots",
                "office wear", "business attire", "formal clothing", "dress shoes"
            ]
            
            # Check for outdoor elements
            outdoor_scores = await clip_service.classify_aesthetics(image_content, outdoor_keywords)
            max_outdoor_score = max([score.score for score in outdoor_scores]) if outdoor_scores else 0
            
            # Check for non-outdoor elements
            non_outdoor_scores = await clip_service.classify_aesthetics(image_content, non_outdoor_keywords)
            max_non_outdoor_score = max([score.score for score in non_outdoor_scores]) if non_outdoor_scores else 0
            
            # Only apply gorpcore boost if outdoor elements are more confident than non-outdoor
            if max_outdoor_score > max_non_outdoor_score and max_outdoor_score > 0.2:
                logger.info(f"✅ GORPCORE CONTEXT VALIDATED: outdoor={max_outdoor_score:.3f} > non-outdoor={max_non_outdoor_score:.3f}")
                return True
            else:
                logger.info(f"🚫 GORPCORE CONTEXT REJECTED: outdoor={max_outdoor_score:.3f} <= non-outdoor={max_non_outdoor_score:.3f}")
                return False
                
        except Exception as e:
            logger.error(f"Error in gorpcore context validation: {str(e)}")
            # Default to rejecting gorpcore boost if validation fails
            return False


# Global service instance
moodboard_service = MoodboardService()