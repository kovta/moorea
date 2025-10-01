"""
Test for gorpcore CLIP embeddings functionality.

This test verifies that the system correctly recognizes gorpcore keywords
and classifies images as gorpcore instead of techwear.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from PIL import Image
import io
import numpy as np

from services.moodboard_service import MoodboardService
from services.clip_service import CLIPService
from services.aesthetic_service import AestheticService
from models import AestheticScore


class TestGorpcoreClassification:
    """Test suite for gorpcore aesthetic classification."""
    
    @pytest.fixture
    def moodboard_service(self):
        """Create a MoodboardService instance for testing."""
        return MoodboardService()
    
    @pytest.fixture
    def clip_service(self):
        """Create a CLIPService instance for testing."""
        return CLIPService()
    
    @pytest.fixture
    def aesthetic_service(self):
        """Create an AestheticService instance for testing."""
        return AestheticService()
    
    @pytest.fixture
    def gorpcore_keywords(self):
        """Return the expected gorpcore keywords."""
        return [
            'hiking wear', 'technical apparel', 'outdoor gear', 'waterproof materials', 
            'durable fabrics', 'cargo pants', 'utility pockets', 'fleece jacket', 
            'hiking boots', 'trail mix', 'functional clothing', 'rugged wear', 
            'practical fashion', 'earthy colors', 'streetwear blend', 'urban hiking', 
            'comfort utility'
        ]
    
    @pytest.fixture
    def mock_gorpcore_image(self):
        """Create a mock image that should be classified as gorpcore."""
        # Create a simple test image (1x1 pixel)
        img = Image.new('RGB', (1, 1), color='brown')
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        return img_bytes.getvalue()
    
    @pytest.mark.asyncio
    async def test_gorpcore_keywords_loaded_correctly(self, aesthetic_service):
        """Test that gorpcore keywords are loaded correctly from aesthetics.yaml."""
        await aesthetic_service.initialize()
        keywords = await aesthetic_service.get_keywords_for_aesthetic('gorpcore')
        
        assert keywords is not None
        assert len(keywords) > 0
        assert 'hiking wear' in keywords
        assert 'technical apparel' in keywords
        assert 'outdoor gear' in keywords
        assert 'cargo pants' in keywords
        assert 'utility pockets' in keywords
    
    @pytest.mark.asyncio
    async def test_clip_uses_gorpcore_keywords_in_prompts(self, clip_service, aesthetic_service):
        """Test that CLIP service creates prompts using gorpcore keywords."""
        await aesthetic_service.initialize()
        
        # Mock the aesthetic service to return gorpcore keywords
        with patch.object(aesthetic_service, 'get_keywords_for_aesthetic') as mock_get_keywords:
            mock_get_keywords.return_value = [
                'hiking wear', 'technical apparel', 'outdoor gear', 
                'waterproof materials', 'durable fabrics'
            ]
            
            # Test the prompt creation
            vocabulary = ['gorpcore', 'techwear', 'streetwear']
            prompts = await clip_service._create_text_prompts(vocabulary)
            
            # Find the gorpcore prompt
            gorpcore_prompt = next((p for p in prompts if 'gorpcore' in p), None)
            
            assert gorpcore_prompt is not None
            assert 'gorpcore aesthetic with' in gorpcore_prompt
            assert 'hiking wear' in gorpcore_prompt
            assert 'technical apparel' in gorpcore_prompt
            assert 'outdoor gear' in gorpcore_prompt
    
    @pytest.mark.asyncio
    async def test_gorpcore_classification_beats_techwear(self, moodboard_service, mock_gorpcore_image):
        """Test that gorpcore images are classified as gorpcore, not techwear."""
        
        # Mock the CLIP service to return realistic scores
        mock_clip_scores = [
            AestheticScore(name="gorpcore", score=0.45, description="Functional rugged outdoor gear"),
            AestheticScore(name="techwear", score=0.35, description="Futuristic technical clothing"),
            AestheticScore(name="streetwear", score=0.15, description="Urban casual style"),
            AestheticScore(name="normcore", score=0.05, description="Basic everyday style")
        ]
        
        with patch('services.moodboard_service.clip_service.classify_aesthetics') as mock_classify:
            mock_classify.return_value = mock_clip_scores
            
            # Mock aesthetic service
            with patch('services.moodboard_service.aesthetic_service.get_vocabulary') as mock_vocab:
                mock_vocab.return_value = ['gorpcore', 'techwear', 'streetwear', 'normcore']
                
                with patch('services.moodboard_service.aesthetic_service.get_aesthetic_description') as mock_desc:
                    mock_desc.return_value = "Test description"
                    
                    # Run the classification
                    result = await moodboard_service._classify_aesthetics(mock_gorpcore_image)
                    
                    # Assertions
                    assert len(result) > 0
                    assert result[0].name == "gorpcore"
                    assert result[0].score >= 0.4  # Should have high confidence
                    
                    # Verify gorpcore beats techwear
                    gorpcore_score = next((a.score for a in result if a.name == "gorpcore"), 0)
                    techwear_score = next((a.score for a in result if a.name == "techwear"), 0)
                    
                    assert gorpcore_score > techwear_score
    
    @pytest.mark.asyncio
    async def test_gorpcore_boost_calculation(self, moodboard_service, mock_gorpcore_image):
        """Test that gorpcore gets appropriate boost from lifestyle category."""
        
        # Mock CLIP to return low initial gorpcore score (should be boosted)
        mock_clip_scores = [
            AestheticScore(name="techwear", score=0.60, description="Futuristic technical clothing"),
            AestheticScore(name="streetwear", score=0.20, description="Urban casual style"),
            AestheticScore(name="gorpcore", score=0.03, description="Functional rugged outdoor gear"),  # Low initial score
            AestheticScore(name="normcore", score=0.02, description="Basic everyday style")
        ]
        
        with patch('services.moodboard_service.clip_service.classify_aesthetics') as mock_classify:
            mock_classify.return_value = mock_clip_scores
            
            with patch('services.moodboard_service.aesthetic_service.get_vocabulary') as mock_vocab:
                mock_vocab.return_value = ['techwear', 'streetwear', 'gorpcore', 'normcore']
                
                with patch('services.moodboard_service.aesthetic_service.get_aesthetic_description') as mock_desc:
                    mock_desc.return_value = "Test description"
                    
                    # Run classification
                    result = await moodboard_service._classify_aesthetics(mock_gorpcore_image)
                    
                    # Check that gorpcore gets boosted appropriately
                    gorpcore_result = next((a for a in result if a.name == "gorpcore"), None)
                    
                    if gorpcore_result:
                        # Gorpcore should have a boosted score (original 0.03 * boost multiplier)
                        assert gorpcore_result.score > 0.03
                        # Should be competitive with techwear after boost
                        assert gorpcore_result.score >= 0.1
    
    @pytest.mark.asyncio
    async def test_gorpcore_keywords_influence_classification(self, aesthetic_service):
        """Test that gorpcore keywords are properly integrated into the classification system."""
        
        await aesthetic_service.initialize()
        
        # Get actual gorpcore keywords
        keywords = await aesthetic_service.get_keywords_for_aesthetic('gorpcore')
        
        # Verify key gorpcore characteristics are present
        expected_keywords = [
            'hiking wear', 'technical apparel', 'outdoor gear', 
            'cargo pants', 'utility pockets', 'fleece jacket',
            'hiking boots', 'functional clothing', 'rugged wear'
        ]
        
        for keyword in expected_keywords:
            assert keyword in keywords, f"Missing expected gorpcore keyword: {keyword}"
        
        # Verify the keywords are comprehensive
        assert len(keywords) >= 10, "Gorpcore should have comprehensive keyword set"
        
        # Verify no techwear-specific keywords are mixed in
        techwear_keywords = ['cyberpunk', 'futuristic', 'neon', 'sci-fi']
        for keyword in techwear_keywords:
            assert keyword not in keywords, f"Techwear keyword should not be in gorpcore: {keyword}"
    
    @pytest.mark.asyncio
    async def test_gorpcore_vs_techwear_distinction(self, moodboard_service):
        """Test that gorpcore and techwear are properly distinguished."""
        
        # Create mock images for both aesthetics
        gorpcore_image = b"mock_gorpcore_image_data"
        techwear_image = b"mock_techwear_image_data"
        
        # Mock CLIP responses for gorpcore image
        gorpcore_scores = [
            AestheticScore(name="gorpcore", score=0.50, description="Functional rugged outdoor gear"),
            AestheticScore(name="techwear", score=0.25, description="Futuristic technical clothing"),
            AestheticScore(name="streetwear", score=0.15, description="Urban casual style")
        ]
        
        # Mock CLIP responses for techwear image  
        techwear_scores = [
            AestheticScore(name="techwear", score=0.55, description="Futuristic technical clothing"),
            AestheticScore(name="gorpcore", score=0.20, description="Functional rugged outdoor gear"),
            AestheticScore(name="streetwear", score=0.15, description="Urban casual style")
        ]
        
        with patch('services.moodboard_service.clip_service.classify_aesthetics') as mock_classify:
            # First call returns gorpcore scores, second call returns techwear scores
            mock_classify.side_effect = [gorpcore_scores, techwear_scores]
            
            with patch('services.moodboard_service.aesthetic_service.get_vocabulary') as mock_vocab:
                mock_vocab.return_value = ['gorpcore', 'techwear', 'streetwear']
                
                with patch('services.moodboard_service.aesthetic_service.get_aesthetic_description') as mock_desc:
                    mock_desc.return_value = "Test description"
                    
                    # Test gorpcore image classification
                    gorpcore_result = await moodboard_service._classify_aesthetics(gorpcore_image)
                    assert gorpcore_result[0].name == "gorpcore"
                    assert gorpcore_result[0].score > 0.4
                    
                    # Test techwear image classification
                    techwear_result = await moodboard_service._classify_aesthetics(techwear_image)
                    assert techwear_result[0].name == "techwear"
                    assert techwear_result[0].score > 0.4


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])
