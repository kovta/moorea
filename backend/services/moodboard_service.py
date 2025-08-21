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
            
            # Step 2: Keyword expansion (placeholder)
            logger.info(f"Expanding keywords for job {job_id}")
            search_keywords = await self._expand_keywords(top_aesthetics)
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
        """Classify image aesthetics using CLIP."""
        try:
            # Get aesthetic vocabulary
            vocabulary = await aesthetic_service.get_vocabulary()
            
            # Use CLIP for zero-shot classification
            scores = await clip_service.classify_aesthetics(image_content, vocabulary)
            
            # Add descriptions from aesthetic service
            for score in scores:
                description = await aesthetic_service.get_aesthetic_description(score.name)
                score.description = description
            
            # Return top 5 aesthetics
            return scores[:5]
            
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
    
    async def _expand_keywords(self, aesthetics: List[AestheticScore]) -> List[str]:
        """Expand aesthetics to search keywords."""
        keywords = []
        for aesthetic in aesthetics:
            aesthetic_keywords = await aesthetic_service.get_keywords_for_aesthetic(aesthetic.name)
            keywords.extend(aesthetic_keywords)
        return keywords
    
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
            
            # Return top candidates (up to final moodboard size)
            final_count = min(len(scored_candidates), settings.final_moodboard_size)
            return scored_candidates[:final_count]
            
        except Exception as e:
            logger.error(f"Error in candidate re-ranking: {str(e)}")
            # Fallback: return first N candidates without scoring
            return candidates[:settings.final_moodboard_size]


# Global service instance
moodboard_service = MoodboardService()