"""Moodboard generation service - orchestrates the full pipeline."""

import asyncio
import logging
from datetime import datetime
from typing import List
from uuid import UUID

from config import settings
from models import JobStatus, MoodboardResult, AestheticScore, ImageCandidate
from services.job_service import job_service
from services.aesthetic_service import aesthetic_service
from services.unsplash_client import unsplash_client
from services.pexels_client import pexels_client
from services.flickr_client import flickr_client
from services.clip_service import clip_service

logger = logging.getLogger(__name__)


class MoodboardService:
    """Service for orchestrating moodboard generation pipeline."""
    
    def __init__(self):
        pass
    
    async def queue_generation(self, job_id: UUID, image_content: bytes, env_images: int | None = None, target_vibe: str | None = None) -> None:
        """Queue moodboard generation job."""
        # For now, process immediately (add proper queue later)
        asyncio.create_task(self._process_moodboard(job_id, image_content, env_images=env_images, target_vibe=target_vibe))
    
    async def _process_moodboard(self, job_id: UUID, image_content: bytes, env_images: int | None = None, target_vibe: str | None = None) -> None:
        """Process moodboard generation pipeline."""
        try:
            await job_service.update_job_status(job_id, JobStatus.PROCESSING, progress=0)
            
            # Step 1: CLIP Classification (placeholder)
            logger.info(f"Starting aesthetic classification for job {job_id}")
            await asyncio.sleep(1)  # Simulate processing
            top_aesthetics = await self._classify_aesthetics(image_content)
            if target_vibe:
                top_aesthetics = await self._apply_vibe_bias(top_aesthetics, target_vibe)
            await job_service.update_job_status(job_id, JobStatus.PROCESSING, progress=25)
            
            # Step 2: Keyword expansion with intelligent filtering
            logger.info(f"Expanding keywords for job {job_id}")
            search_keywords, negative_keywords = await self._expand_keywords(top_aesthetics)
            # Strengthen negatives based on vibe
            if target_vibe:
                vibe_negatives = self._vibe_negative_keywords(target_vibe)
                negative_keywords = list(set(negative_keywords) | set(vibe_negatives))
                # Remove negatives from keywords proactively
                search_keywords = [k for k in search_keywords if not any(n in k.lower() for n in vibe_negatives)]
            logger.info(f"Generated {len(search_keywords)} search keywords, avoiding {len(negative_keywords)} negative terms")
            await job_service.update_job_status(job_id, JobStatus.PROCESSING, progress=50)
            
            # Step 3: Fetch clothing-focused candidates
            logger.info(f"Fetching image candidates for job {job_id}")
            candidates = await self._fetch_candidates(search_keywords)
            await job_service.update_job_status(job_id, JobStatus.PROCESSING, progress=75)
            
            # Step 4: Re-rank and select clothing images
            logger.info(f"Re-ranking candidates for job {job_id}")
            clothing_ranked = await self._rerank_candidates(image_content, candidates)

            # Optional: fetch a dedicated environment pool and merge a fixed count
            final_images = clothing_ranked
            if env_images is not None and env_images > 0:
                logger.info(f"Env images requested: {env_images}")
                env_pool = await self._fetch_environment_pool(top_aesthetics=top_aesthetics)
                final_images = self._merge_with_environment(clothing_ranked, env_pool, env_images)
            await job_service.update_job_status(job_id, JobStatus.PROCESSING, progress=100)
            
            # Store result
            result = MoodboardResult(
                job_id=job_id,
                status=JobStatus.COMPLETED,
                top_aesthetics=top_aesthetics,
                images=final_images,
                created_at=datetime.now(),
                processing_time=5.0  # placeholder
            )
            
            await job_service.store_job_result(job_id, result)
            logger.info(f"Completed moodboard generation for job {job_id}")
            
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
            # Get aesthetic vocabulary
            vocabulary = await aesthetic_service.get_vocabulary()
            
            # Use CLIP for zero-shot classification
            all_scores = await clip_service.classify_aesthetics(image_content, vocabulary)
            
            # Add descriptions from aesthetic service
            for score in all_scores:
                description = await aesthetic_service.get_aesthetic_description(score.name)
                score.description = description
            
            # Log detailed classification results
            logger.info("=== CLIP Classification Results ===")
            for i, score in enumerate(all_scores[:10]):  # Show top 10 to find cottagecore
                logger.info(f"#{i+1}: {score.name} = {score.score:.3f} ({score.score*100:.1f}%)")
            logger.info("===================================")

            # Focus on the dominant (highest confidence) aesthetic
            dominant_aesthetic = all_scores[0]
            logger.info(f"Selected dominant aesthetic: {dominant_aesthetic.name} ({dominant_aesthetic.score:.3f})")
            
            # Apply intelligent threshold logic
            MINIMUM_CONFIDENCE_THRESHOLD = 0.025  # 2.5% - lowered since lifestyle boost works effectively
            logger.info(f"🏆 HIGHEST CONFIDENCE AESTHETIC: {dominant_aesthetic.name} at {dominant_aesthetic.score:.3f} ({dominant_aesthetic.score*100:.1f}%)")
            
            # Special logic: Prefer lifestyle aesthetics over bridal if they're close
            lifestyle_aesthetics = ["cottagecore", "fairycore", "goblincore", "clean_girl", "soft_girl", "coquette", "vintage", "retro"]
            for aesthetic in all_scores[:10]:  # Check top 10
                if aesthetic.name in lifestyle_aesthetics and aesthetic.score >= 0.025:  # 2.5% minimum
                    if aesthetic.score * 6.0 >= dominant_aesthetic.score:  # Give 600% boost to lifestyle aesthetics
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
            
            if dominant_aesthetic.score < MINIMUM_CONFIDENCE_THRESHOLD:
                logger.warning(f"❌ REJECTED: '{dominant_aesthetic.name}' confidence ({dominant_aesthetic.score:.3f}) below threshold ({MINIMUM_CONFIDENCE_THRESHOLD})")
                logger.info("Falling back to generic 'minimalist' aesthetic for broad inspiration")
                fallback_aesthetic = AestheticScore(name="minimalist", score=0.65, description="Clean, versatile style that works with many pieces")
                return [fallback_aesthetic]
            
            logger.info(f"✅ ACCEPTED: '{dominant_aesthetic.name}' confidence ({dominant_aesthetic.score:.3f}) meets threshold ({MINIMUM_CONFIDENCE_THRESHOLD})")
            
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
        
        for aesthetic in aesthetics:
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
        
        # Remove duplicates and apply negative filtering
        unique_keywords = []
        for keyword in keywords:
            # Skip if keyword contains negative terms
            if not any(neg in keyword.lower() for neg in negative_keywords):
                unique_keywords.append(keyword)
        
        return unique_keywords, list(negative_keywords)

    async def _apply_vibe_bias(self, scores: List[AestheticScore], vibe: str) -> List[AestheticScore]:
        """Boost/demote aesthetics based on a target vibe."""
        if not scores:
            return scores
        vibe = (vibe or "").lower()
        boosts: dict[str, float] = {}
        demotes: dict[str, float] = {}

        if vibe in ("nancy_meyers", "nancy-meyers", "nancy_meyers_aesthetic"):
            boosts = {
                "quiet_luxury": 2.0,
                "old_money": 1.8,
                "preppy": 1.6,
                "minimalist": 1.5,
                "coastal": 1.7,
                "coastal_grandmother": 2.0,
            }
            demotes = {
                "mob_wife": 0.4,
                "grunge": 0.5,
                "maximalist": 0.6,
                "bridal_ballgown": 0.6,
                "bridal_mermaid": 0.6,
                "bridal_artdeco": 0.6,
                "bridal_princess": 0.6,
                "bridal_romantic": 0.7,
            }

        adjusted: List[AestheticScore] = []
        for s in scores:
            factor = 1.0
            if s.name in boosts:
                factor = boosts[s.name]
            if s.name in demotes:
                factor = demotes[s.name]
            adjusted.append(AestheticScore(name=s.name, score=min(1.0, s.score * factor), description=s.description))

        adjusted.sort(key=lambda x: x.score, reverse=True)
        return adjusted[:3]

    def _vibe_negative_keywords(self, vibe: str) -> List[str]:
        vibe = (vibe or "").lower()
        if vibe in ("nancy_meyers", "nancy-meyers", "nancy_meyers_aesthetic"):
            return [
                "sexy", "club", "bodycon", "neon", "gothic", "punk", "streetwear",
                "maximalist", "leather jacket", "dark makeup", "fishnets"
            ]
        return []
    
    async def _fetch_candidates(self, keywords: List[str]) -> List[ImageCandidate]:
        """Fetch image candidates from all APIs."""
        all_candidates = []
        images_per_keyword = max(1, 50 // len(keywords)) if keywords else 5
        
        # Fetch from all APIs concurrently
        for keyword in keywords[:5]:  # Limit to top 5 keywords to stay within rate limits
            tasks = [
                unsplash_client.search_photos(keyword, per_page=images_per_keyword),
                pexels_client.search_photos(keyword, per_page=images_per_keyword),
                flickr_client.search_photos(keyword, per_page=images_per_keyword)
            ]
            
            # Execute all API calls concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, list):  # Successful result
                    all_candidates.extend(result)
                else:
                    logger.error(f"API call failed: {result}")
        
        # Remove duplicates by URL and limit total
        seen_urls = set()
        unique_candidates = []
        for candidate in all_candidates:
            if candidate.url not in seen_urls:
                seen_urls.add(candidate.url)
                unique_candidates.append(candidate)
                if len(unique_candidates) >= 50:  # Limit total candidates
                    break
        
        logger.info(f"Fetched {len(unique_candidates)} unique candidates from all APIs")
        return unique_candidates
    
    async def _rerank_candidates(self, original_image: bytes, 
                                candidates: List[ImageCandidate]) -> List[ImageCandidate]:
        """Re-rank candidates using CLIP similarity."""
        try:
            if not candidates:
                return []
            
            # Get original image embedding
            original_embedding = await clip_service.get_image_embedding(original_image)
            
            # Calculate similarities for all candidates
            candidate_urls = [c.url for c in candidates]
            similarities = await clip_service.batch_similarity(original_embedding, candidate_urls)
            
            # Add similarity scores and sort by score
            scored_candidates = []
            for candidate, similarity in zip(candidates, similarities):
                candidate.similarity_score = similarity
                scored_candidates.append(candidate)
            
            # Sort by similarity score (highest first)
            scored_candidates.sort(key=lambda x: x.similarity_score or 0, reverse=True)
            
            # Filter by minimum similarity threshold (60%)
            MIN_SIMILARITY_THRESHOLD = 0.60
            filtered_candidates = [
                candidate for candidate in scored_candidates 
                if (candidate.similarity_score or 0) >= MIN_SIMILARITY_THRESHOLD
            ]
            
            logger.info(f"Filtered {len(scored_candidates)} candidates to {len(filtered_candidates)} above {MIN_SIMILARITY_THRESHOLD} similarity")
            
            # Return filtered candidates (up to final moodboard size)
            if len(filtered_candidates) >= 3:  # Need at least 3 good matches
                final_count = min(len(filtered_candidates), settings.final_moodboard_size)
                return filtered_candidates[:final_count]
            else:
                # Fallback: if too few high-quality matches, lower threshold to 50%
                logger.warning(f"Only {len(filtered_candidates)} high-quality matches, using 50% threshold")
                fallback_candidates = [
                    candidate for candidate in scored_candidates 
                    if (candidate.similarity_score or 0) >= 0.50
                ]
                final_count = min(len(fallback_candidates), settings.final_moodboard_size)
                return fallback_candidates[:final_count]
            
        except Exception as e:
            logger.error(f"Error in candidate re-ranking: {str(e)}")
            # Fallback: return first N candidates without scoring
            return candidates[:settings.final_moodboard_size]

    async def _fetch_environment_pool(self, top_aesthetics: List[AestheticScore]) -> List[ImageCandidate]:
        """Fetch a pool of environment images using Pexels only, tagged as environment.
        This pool is independent of clothing similarity to guarantee availability.
        """
        # Default cross-aesthetic environment keywords (Nancy Meyers/clean interiors friendly)
        base_env_keywords = [
            "sunlit kitchen",
            "cozy living room",
            "neutral interior",
            "garden party",
            "coastal house",
            "linen curtains",
            "soft lighting"
        ]

        # Bias by detected aesthetics
        aesthetic_names = [a.name for a in top_aesthetics]
        if any(name in aesthetic_names for name in ["coastal", "coastal_grandmother", "old_money", "quiet_luxury", "preppy", "minimalist"]):
            base_env_keywords.extend(["hampton style home", "light wood kitchen", "white marble kitchen"])

        env_candidates: List[ImageCandidate] = []
        per_keyword = 6
        for keyword in base_env_keywords:
            try:
                results = await pexels_client.search_photos(keyword, per_page=per_keyword)
                for c in results:
                    c.category = "environment"
                env_candidates.extend(results)
            except Exception as e:
                logger.error(f"Environment fetch failed for '{keyword}': {e}")

        # De-duplicate by URL
        seen = set()
        unique_env: List[ImageCandidate] = []
        for c in env_candidates:
            if c.url not in seen:
                seen.add(c.url)
                unique_env.append(c)

        logger.info(f"Environment pool size: {len(unique_env)}")
        return unique_env

    def _merge_with_environment(self, clothing_ranked: List[ImageCandidate], env_pool: List[ImageCandidate], env_count: int) -> List[ImageCandidate]:
        """Merge a fixed number of environment images into the final set.
        - Keep clothing order by similarity
        - Take env_count from env_pool in order
        - Do not drop below env_count if available
        """
        if env_count <= 0:
            return clothing_ranked[:settings.final_moodboard_size]

        total_needed = settings.final_moodboard_size
        env_pick = env_pool[:env_count] if env_pool else []
        remaining_slots = max(0, total_needed - len(env_pick))
        clothing_pick = clothing_ranked[:remaining_slots]

        # Interleave: start with up to 2 clothing, then alternate
        result: List[ImageCandidate] = []
        c_idx = 0
        e_idx = 0

        while c_idx < len(clothing_pick) and len(result) < 2:
            result.append(clothing_pick[c_idx])
            c_idx += 1

        while len(result) < total_needed and (c_idx < len(clothing_pick) or e_idx < len(env_pick)):
            if e_idx < len(env_pick):
                result.append(env_pick[e_idx])
                e_idx += 1
            if len(result) >= total_needed:
                break
            if c_idx < len(clothing_pick):
                result.append(clothing_pick[c_idx])
                c_idx += 1

        # Fill trailing
        for tail in (clothing_pick[c_idx:], env_pick[e_idx:]):
            for item in tail:
                if len(result) >= total_needed:
                    break
                result.append(item)

        logger.info(f"Merged environment images: {min(len(env_pick), env_count)} of requested {env_count}")
        return result

    def _apply_environment_mix(self, ranked: List[ImageCandidate], desired_env: int) -> List[ImageCandidate]:
        """Ensure the final list contains up to desired_env environment images by heuristics.
        If category is missing, infer via simple keyword heuristics in URL.
        """
        if not ranked:
            return ranked
        desired_env = max(0, min(desired_env, settings.final_moodboard_size))

        clothing_keywords = [
            "dress", "skirt", "shirt", "blouse", "pants", "jeans", "jacket", "coat",
            "outfit", "sweater", "cardigan", "top", "tee", "heels", "boots", "sneakers"
        ]
        environment_keywords = [
            "field", "forest", "cabin", "room", "interior", "architecture", "beach",
            "ocean", "mountain", "garden", "flowers", "landscape", "venue", "wedding",
            "city", "street", "library", "studio"
        ]

        def infer_category(c: ImageCandidate) -> str:
            if c.category:
                return c.category
            url = (c.url or "").lower()
            if any(k in url for k in clothing_keywords):
                return "clothing"
            if any(k in url for k in environment_keywords):
                return "environment"
            # Default to clothing so we only add environment when confident
            return "clothing"

        clothing: List[ImageCandidate] = []
        environment: List[ImageCandidate] = []
        for c in ranked:
            (environment if infer_category(c) == "environment" else clothing).append(c)

        # Start with best clothing, then interleave environment up to desired_env
        result: List[ImageCandidate] = []
        env_added = 0
        c_idx = 0
        e_idx = 0
        total_needed = min(len(ranked), settings.final_moodboard_size)

        while len(result) < total_needed and (c_idx < len(clothing) or e_idx < len(environment)):
            # Always try to keep clothing majority; insert env until cap
            if env_added < desired_env and e_idx < len(environment):
                result.append(environment[e_idx])
                env_added += 1
                e_idx += 1
                if len(result) >= total_needed:
                    break
            if c_idx < len(clothing):
                result.append(clothing[c_idx])
                c_idx += 1

        # Fill remaining slots with whichever category has items left
        for tail in (clothing[c_idx:], environment[e_idx:]):
            for item in tail:
                if len(result) >= total_needed:
                    break
                result.append(item)

        return result


# Global service instance
moodboard_service = MoodboardService()