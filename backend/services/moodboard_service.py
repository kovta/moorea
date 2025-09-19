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
    
    async def queue_generation(self, job_id: UUID, image_content: bytes) -> None:
        """Queue moodboard generation job."""
        # For now, process immediately (add proper queue later)
        asyncio.create_task(self._process_moodboard(job_id, image_content))
    
    async def _process_moodboard(self, job_id: UUID, image_content: bytes) -> None:
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
            candidates = await self._fetch_candidates(search_keywords)
            await job_service.update_job_status(job_id, JobStatus.PROCESSING, progress=75)
            
            # Step 4: Re-rank and select (placeholder)
            logger.info(f"Re-ranking candidates for job {job_id}")
            final_images = await self._rerank_candidates(image_content, candidates)
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
            
            # ⚡ STREAMLINED BOOST LOGIC - Single pass for speed
            lifestyle_aesthetics = {"cottagecore", "fairycore", "goblincore", "clean_girl", "soft_girl", "coquette", "vintage", "retro"}
            preppy_aesthetics = {"preppy", "old_money", "quiet_luxury"}
            confused_aesthetics = {"mod", "grunge", "maximalist", "streetwear"}
            dramatic_bridal_aesthetics = {"bridal_ballgown", "bridal_princess", "bridal_mermaid", "bridal_romantic", "bridal_artdeco"}
            
            best_aesthetic = dominant_aesthetic
            best_score = dominant_aesthetic.score
            
            # Single efficient pass through top 10 (max 20 for preppy)
            for i, aesthetic in enumerate(all_scores[:10]):
                # Lifestyle boost (6x)
                if aesthetic.name in lifestyle_aesthetics and aesthetic.score >= 0.025:
                    boosted = aesthetic.score * 6.0
                    if boosted > best_score:
                        logger.info(f"⚡ LIFESTYLE: {aesthetic.name} ({aesthetic.score:.3f} × 6 = {boosted:.3f})")
                        best_aesthetic, best_score = aesthetic, boosted
                
                # Dramatic bridal boost (5x) - promote ballgown/princess over minimalist
                elif aesthetic.name in dramatic_bridal_aesthetics and aesthetic.score >= 0.02:
                    boosted = aesthetic.score * 5.0
                    if boosted > best_score:
                        logger.info(f"⚡ DRAMATIC BRIDAL: {aesthetic.name} ({aesthetic.score:.3f} × 5 = {boosted:.3f})")
                        best_aesthetic, best_score = aesthetic, boosted
                
                # Non-bridal boost (4x) - only if current dominant is bridal_minimalist specifically
                # Don't demote dramatic bridal styles like ballgown/princess
                elif (dominant_aesthetic.name == "bridal_minimalist" and 
                      aesthetic.name == "minimalist" and 
                      aesthetic.score >= 0.03):
                    boosted = aesthetic.score * 4.0
                    if boosted > best_score:
                        logger.info(f"⚡ NON-BRIDAL: {aesthetic.name} ({aesthetic.score:.3f} × 4 = {boosted:.3f})")
                        best_aesthetic, best_score = aesthetic, boosted
            
            # Quick preppy check only if needed (top 20)
            if dominant_aesthetic.name in confused_aesthetics:
                for aesthetic in all_scores[10:20]:  # Check remaining in top 20
                    if aesthetic.name in preppy_aesthetics and aesthetic.score >= 0.01:
                        boosted = aesthetic.score * 8.0
                        if boosted > best_score:
                            logger.info(f"⚡ PREPPY: {aesthetic.name} ({aesthetic.score:.3f} × 8 = {boosted:.3f})")
                            best_aesthetic = aesthetic
                            break
            
            dominant_aesthetic = best_aesthetic
            
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
    
    async def _fetch_candidates(self, keywords: List[str]) -> List[ImageCandidate]:
        """Fetch image candidates from APIs - optimized for speed."""
        all_candidates = []
        
        # ⚡ BALANCED OPTIMIZATION: More images but still fast
        top_keywords = keywords[:4]  # Increased to 4 keywords for more variety
        images_per_keyword = max(3, settings.max_candidates // len(top_keywords)) if top_keywords else 6
        
        # ⚡ Use only 2 fastest APIs (remove Flickr which is often slower)
        all_tasks = []
        for keyword in top_keywords:
            # Reduced timeout for faster failure
            tasks = [
                unsplash_client.search_photos(keyword, per_page=images_per_keyword),
                pexels_client.search_photos(keyword, per_page=images_per_keyword)
                # Removed Flickr for speed
            ]
            all_tasks.extend(tasks)
        
        # Execute all API calls concurrently with shorter timeout
        logger.info(f"⚡ Fetching from 2 APIs for {len(top_keywords)} keywords ({len(all_tasks)} total requests)")
        
        try:
            # Use asyncio.wait_for with timeout to prevent hanging
            results = await asyncio.wait_for(
                asyncio.gather(*all_tasks, return_exceptions=True),
                timeout=8.0  # Max 8 seconds for all API calls
            )
            
            for result in results:
                if isinstance(result, list):  # Successful result
                    all_candidates.extend(result)
                elif not isinstance(result, asyncio.TimeoutError):
                    logger.warning(f"API call failed: {result}")
                    
        except asyncio.TimeoutError:
            logger.warning("⚠️ API calls timed out after 8 seconds, using partial results")
        
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


# Global service instance
moodboard_service = MoodboardService()