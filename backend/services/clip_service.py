"""CLIP model service for aesthetic classification and image similarity."""

import logging
import hashlib
from io import BytesIO
from typing import Dict, List, Tuple, Optional
import asyncio
import numpy as np
from PIL import Image
import torch
import clip
from transformers import CLIPProcessor, CLIPModel

from config import settings
from models import AestheticScore
from services.cache_service import cache_service

logger = logging.getLogger(__name__)


class CLIPService:
    """Service for CLIP-based aesthetic classification and similarity."""
    
    def __init__(self):
        self.model = None
        self.processor = None
        self.device = None
        self._model_loaded = False
        self._text_embeddings_cache = {}  # Cache for pre-computed text embeddings
    
    async def initialize(self):
        """Initialize CLIP model."""
        try:
            logger.info(f"Loading CLIP model: {settings.clip_model_name}")
            
            # Determine device
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"Using device: {self.device}")
            
            # Load model asynchronously in thread pool to avoid blocking
            await asyncio.get_event_loop().run_in_executor(
                None, self._load_model
            )
            
            logger.info("CLIP model loaded successfully")
            self._model_loaded = True
            
            # Pre-compute text embeddings for performance
            await self._precompute_text_embeddings()
            
        except Exception as e:
            logger.error(f"Failed to load CLIP model: {str(e)}")
            raise
    
    async def _precompute_text_embeddings(self):
        """Pre-compute and cache text embeddings for all aesthetics."""
        try:
            from services.aesthetic_service import aesthetic_service
            
            # Get aesthetic vocabulary
            vocabulary = await aesthetic_service.get_vocabulary()
            logger.info(f"Pre-computing text embeddings for {len(vocabulary)} aesthetics...")
            
            # Create text prompts using actual keywords
            text_prompts = await self._create_text_prompts(vocabulary)
            
            # Tokenize and encode in one batch for efficiency
            text_tokens = clip.tokenize(text_prompts).to(self.device)
            
            with torch.no_grad():
                text_features = self.model.encode_text(text_tokens)
                text_features /= text_features.norm(dim=-1, keepdim=True)
            
            # Cache embeddings by aesthetic name
            for i, aesthetic in enumerate(vocabulary):
                self._text_embeddings_cache[aesthetic] = text_features[i:i+1]
            
            logger.info(f"✅ Pre-computed {len(vocabulary)} text embeddings for faster classification")
            
        except Exception as e:
            logger.warning(f"Failed to pre-compute text embeddings: {str(e)}")
            # Continue without pre-computed embeddings (fallback to on-demand)
    
    def _load_model(self):
        """Load the CLIP model (blocking operation)."""
        # Using OpenAI's CLIP implementation
        self.model, self.processor = clip.load(settings.clip_model_name, device=self.device)
        self.model.eval()  # Set to evaluation mode
    
    def _preprocess_image(self, image_content: bytes) -> torch.Tensor:
        """Preprocess image for CLIP."""
        try:
            # Open and convert image
            image = Image.open(BytesIO(image_content))
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Preprocess with CLIP processor
            image_input = self.processor(image).unsqueeze(0).to(self.device)
            
            return image_input
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise
    
    async def _create_text_prompts(self, aesthetic_terms: List[str]) -> List[str]:
        """Create text prompts for zero-shot classification using actual keywords."""
        from services.aesthetic_service import aesthetic_service
        
        prompts = []
        for term in aesthetic_terms:
            # Get keywords for this aesthetic
            keywords = await aesthetic_service.get_keywords_for_aesthetic(term)
            
            if keywords:
                # Use the first few keywords to create a rich prompt
                keyword_text = ", ".join(keywords[:5])  # Use first 5 keywords
                prompt = f"{term.replace('_', ' ')} aesthetic with {keyword_text}"
                
                # Debug logging for gorpcore
                if term == "gorpcore":
                    logger.info(f"🎯 GORPCORE PROMPT: '{prompt}'")
                    logger.info(f"🎯 GORPCORE KEYWORDS: {keywords}")
            else:
                # Fallback to simple template if no keywords
                prompt = f"a {term.replace('_', ' ')} style outfit"
                
                # Debug logging for gorpcore
                if term == "gorpcore":
                    logger.warning(f"❌ GORPCORE NO KEYWORDS: '{prompt}'")
            
            prompts.append(prompt)
        
        return prompts
    
    async def classify_aesthetics(self, 
                                image_content: bytes, 
                                aesthetic_vocabulary: List[str]) -> List[AestheticScore]:
        """
        Classify image aesthetics using CLIP zero-shot classification.
        
        Args:
            image_content: Raw image bytes
            aesthetic_vocabulary: List of aesthetic terms to classify against
            
        Returns:
            List of aesthetic scores sorted by confidence
        """
        if not self._model_loaded:
            raise RuntimeError("CLIP model not initialized")
        
        # Check cache first
        cached_result = await cache_service.get_classification_cache(image_content)
        if cached_result:
            return [AestheticScore(**score) for score in cached_result]
        
        try:
            # Run classification in thread pool to avoid blocking
            scores = await asyncio.get_event_loop().run_in_executor(
                None, self._classify_sync, image_content, aesthetic_vocabulary
            )
            
            # Cache the result
            score_dicts = [score.dict() for score in scores]
            await cache_service.set_classification_cache(image_content, score_dicts)
            
            return scores
            
        except Exception as e:
            logger.error(f"Error in aesthetic classification: {str(e)}")
            raise
    
    def _classify_sync(self, image_content: bytes, aesthetic_vocabulary: List[str]) -> List[AestheticScore]:
        """Synchronous CLIP classification using cached text embeddings."""
        # Preprocess image
        image_input = self._preprocess_image(image_content)
        
        # Generate image embedding
        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
            image_features /= image_features.norm(dim=-1, keepdim=True)
        
        # Use cached text embeddings if available, otherwise compute on-demand
        if self._text_embeddings_cache:
            # Fast path: use pre-computed embeddings
            text_features_list = []
            valid_aesthetics = []
            
            for aesthetic in aesthetic_vocabulary:
                if aesthetic in self._text_embeddings_cache:
                    text_features_list.append(self._text_embeddings_cache[aesthetic])
                    valid_aesthetics.append(aesthetic)
            
            if text_features_list:
                # Stack cached embeddings
                text_features = torch.cat(text_features_list, dim=0)
                aesthetic_vocabulary = valid_aesthetics
            else:
                # Fallback to on-demand computation
                text_features = self._compute_text_features_on_demand(aesthetic_vocabulary)
        else:
            # Fallback: compute text embeddings on-demand
            text_features = self._compute_text_features_on_demand(aesthetic_vocabulary)
        
        # Calculate similarities
        with torch.no_grad():
            similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)
            
        # Convert to AestheticScore objects
        scores = []
        for i, (term, score) in enumerate(zip(aesthetic_vocabulary, similarity[0])):
            scores.append(AestheticScore(
                name=term,
                score=float(score),
                description=None  # Can be filled by aesthetic_service later
            ))
        
        # Sort by score descending
        scores.sort(key=lambda x: x.score, reverse=True)
        
        logger.info(f"⚡ Fast classification - Top 3: {[(s.name, f'{s.score:.3f}') for s in scores[:3]]}")
        return scores
    
    def _compute_text_features_on_demand(self, aesthetic_vocabulary: List[str]) -> torch.Tensor:
        """Compute text features on-demand (fallback when cache is not available)."""
        text_prompts = self._create_text_prompts(aesthetic_vocabulary)
        text_tokens = clip.tokenize(text_prompts).to(self.device)
        
        with torch.no_grad():
            text_features = self.model.encode_text(text_tokens)
            text_features /= text_features.norm(dim=-1, keepdim=True)
        
        return text_features
    
    async def calculate_image_similarity(self, 
                                       image1_content: bytes, 
                                       image2_url: str) -> float:
        """
        Calculate similarity between two images using CLIP embeddings.
        
        Args:
            image1_content: Raw bytes of first image
            image2_url: URL of second image to compare
            
        Returns:
            Similarity score between 0 and 1
        """
        if not self._model_loaded:
            raise RuntimeError("CLIP model not initialized")
        
        try:
            return await asyncio.get_event_loop().run_in_executor(
                None, self._similarity_sync, image1_content, image2_url
            )
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            return 0.0
    
    def _similarity_sync(self, image1_content: bytes, image2_url: str) -> float:
        """Synchronous image similarity calculation."""
        try:
            import requests
            
            # Get second image
            response = requests.get(image2_url, timeout=10)
            response.raise_for_status()
            image2_content = response.content
            
            # Process both images
            image1_input = self._preprocess_image(image1_content)
            image2_input = self._preprocess_image(image2_content)
            
            # Generate embeddings
            with torch.no_grad():
                image1_features = self.model.encode_image(image1_input)
                image2_features = self.model.encode_image(image2_input)
                
                # Normalize
                image1_features /= image1_features.norm(dim=-1, keepdim=True)
                image2_features /= image2_features.norm(dim=-1, keepdim=True)
                
                # Calculate cosine similarity
                similarity = torch.cosine_similarity(image1_features, image2_features)
                
            return float(similarity.item())
            
        except Exception as e:
            logger.error(f"Error in similarity calculation: {str(e)}")
            return 0.0
    
    async def get_image_embedding(self, image_content: bytes) -> np.ndarray:
        """Get CLIP embedding for an image."""
        if not self._model_loaded:
            raise RuntimeError("CLIP model not initialized")
        
        try:
            return await asyncio.get_event_loop().run_in_executor(
                None, self._embedding_sync, image_content
            )
            
        except Exception as e:
            logger.error(f"Error getting image embedding: {str(e)}")
            raise
    
    def _embedding_sync(self, image_content: bytes) -> np.ndarray:
        """Synchronous image embedding extraction."""
        image_input = self._preprocess_image(image_content)
        
        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
            image_features /= image_features.norm(dim=-1, keepdim=True)
            
        return image_features.cpu().numpy()[0]
    
    async def batch_similarity(self, 
                             original_embedding: np.ndarray,
                             candidate_urls: List[str]) -> List[float]:
        """
        Calculate similarity scores for multiple candidates efficiently.
        
        Args:
            original_embedding: Pre-computed embedding of original image
            candidate_urls: List of candidate image URLs
            
        Returns:
            List of similarity scores in same order as input URLs
        """
        if not self._model_loaded:
            raise RuntimeError("CLIP model not initialized")
        
        try:
            return await asyncio.get_event_loop().run_in_executor(
                None, self._batch_similarity_sync, original_embedding, candidate_urls
            )
            
        except Exception as e:
            logger.error(f"Error in batch similarity: {str(e)}")
            return [0.0] * len(candidate_urls)
    
    def _batch_similarity_sync(self, 
                              original_embedding: np.ndarray,
                              candidate_urls: List[str]) -> List[float]:
        """Synchronous batch similarity calculation."""
        import requests
        
        similarities = []
        original_tensor = torch.from_numpy(original_embedding).unsqueeze(0).to(self.device)
        
        for url in candidate_urls:
            try:
                # Fetch image with timeout
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                
                # Process image
                candidate_input = self._preprocess_image(response.content)
                
                with torch.no_grad():
                    candidate_features = self.model.encode_image(candidate_input)
                    candidate_features /= candidate_features.norm(dim=-1, keepdim=True)
                    
                    # Calculate similarity
                    similarity = torch.cosine_similarity(original_tensor, candidate_features)
                    similarities.append(float(similarity.item()))
                    
            except Exception as e:
                logger.warning(f"Failed to process candidate {url}: {str(e)}")
                similarities.append(0.0)
        
        return similarities


# Global service instance
clip_service = CLIPService()