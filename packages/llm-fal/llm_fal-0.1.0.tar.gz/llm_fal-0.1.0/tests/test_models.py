"""
Tests for model discovery and execution.
"""

import pytest
import asyncio
from unittest.mock import patch, MagicMock

# Import the module to test - directly from llm_fal
from llm_fal import (
    get_all_models, 
    get_model_category, 
    get_models_by_category,
    search_models,
    get_model_schema,
    MODEL_CATEGORIES
)

# Import test fixtures for sample data
from .fixtures.responses import MODELS_RESPONSE

# Sample model data for testing
SAMPLE_MODELS = MODELS_RESPONSE["models"]

# Tests for get_all_models
@pytest.mark.asyncio
async def test_get_all_models():
    """Test fetching all models."""
    # Mock the fal_client.list_models_async method
    with patch('llm_fal.fal_client.list_models_async') as mock_get:
        # Configure the mock to return sample data
        mock_get.return_value = {"models": SAMPLE_MODELS}
        
        # Call the function
        result = await get_all_models()
        
        # Check the result
        assert result == SAMPLE_MODELS
        mock_get.assert_called_once()

@pytest.mark.asyncio
async def test_get_all_models_cached():
    """Test that models are cached."""
    # Mock the fal_client.list_models_async method
    with patch('llm_fal.fal_client.list_models_async') as mock_get:
        # Configure the mock to return sample data
        mock_get.return_value = {"models": SAMPLE_MODELS}
        
        # Set up the cache
        from llm_fal import _model_cache
        _model_cache["all_models"] = SAMPLE_MODELS
        
        # Call the function
        result = await get_all_models()
        
        # Check that the result comes from cache
        assert result == SAMPLE_MODELS
        mock_get.assert_not_called()
        
        # Clear the cache for other tests
        _model_cache.clear()

@pytest.mark.asyncio
async def test_get_all_models_error():
    """Test handling of API errors."""
    # Mock the fal_client.list_models_async method to raise an exception
    with patch('llm_fal.fal_client.list_models_async', side_effect=Exception("API Error")):
        # Call the function
        result = await get_all_models()
        
        # Check that an empty list is returned on error
        assert result == []

# Tests for get_model_category
def test_get_model_category():
    """Test categorizing models."""
    # Test image category
    assert get_model_category({"id": "fal-ai/stable-diffusion/v1-5"}) == "image"
    assert get_model_category({"id": "fal-ai/flux-pro/v1.1-ultra"}) == "image"
    
    # Test newer image models
    assert get_model_category({"id": "fal-ai/flux/dev"}) == "image"
    assert get_model_category({"id": "fal-ai/flux/schnell"}) == "image"
    assert get_model_category({"id": "fal-ai/esrgan"}) == "image"
    
    # Test audio category
    assert get_model_category({"id": "fal-ai/playai/tts/dialog"}) == "audio"
    
    # Test video category
    assert get_model_category({"id": "fal-ai/wan-pro/image-to-video"}) == "video"
    
    # Test text category
    assert get_model_category({"id": "fal-ai/text-generation/llm"}) == "text"
    
    # Test custom category
    assert get_model_category({"id": "fal-ai/custom-model/v1"}) == "custom"
    
    # Test other category (fallback)
    assert get_model_category({"id": "fal-ai/unknown-model-type"}) == "other"

# Tests for get_models_by_category
def test_get_models_by_category():
    """Test grouping models by category."""
    # Mock the get_all_models function
    with patch('llm_fal.asyncio.run') as mock_run:
        # Configure the mock to return sample data
        mock_run.return_value = SAMPLE_MODELS
        
        # Call the function
        result = get_models_by_category()
        
        # Check the result structure
        assert isinstance(result, dict)
        assert all(category in result for category in MODEL_CATEGORIES.keys())
        
        # Check that models are properly categorized
        assert len(result["image"]) > 0  # Should have some image models
        assert len(result["audio"]) > 0  # Should have some audio models
        assert len(result["video"]) > 0  # Should have some video models

# Tests for search_models
def test_search_models():
    """Test searching for models by keyword."""
    # Mock the get_all_models function
    with patch('llm_fal.asyncio.run') as mock_run:
        # Configure the mock to return sample data
        mock_run.return_value = SAMPLE_MODELS
        
        # Test search with matching query
        result = search_models("stable")
        assert len(result) == 1
        assert result[0]["id"] == "fal-ai/stable-diffusion/v1-5"
        
        # Test search in description
        result = search_models("high-resolution")
        assert len(result) == 1
        assert result[0]["id"] == "fal-ai/flux-pro/v1.1-ultra"
        
        # Test search with no matches
        result = search_models("nonexistent")
        assert len(result) == 0

# Tests for get_model_schema
@pytest.mark.asyncio
async def test_get_model_schema():
    """Test fetching model schema."""
    # Import test fixture for sample schema
    from .fixtures.responses import MODEL_SCHEMA_RESPONSE
    
    # Mock the fal_client.get_model_schema_async method
    with patch('llm_fal.fal_client.get_model_schema_async') as mock_get:
        # Configure the mock to return sample data
        mock_get.return_value = MODEL_SCHEMA_RESPONSE
        
        # Call the function
        result = await get_model_schema("fal-ai/stable-diffusion/v1-5")
        
        # Check the result
        assert result == MODEL_SCHEMA_RESPONSE
        mock_get.assert_called_once_with("fal-ai/stable-diffusion/v1-5")

@pytest.mark.asyncio
async def test_get_model_schema_error():
    """Test handling of API errors."""
    # Mock the fal_client.get_model_schema_async method to raise an exception
    with patch('llm_fal.fal_client.get_model_schema_async', side_effect=Exception("API Error")):
        # Call the function
        result = await get_model_schema("fal-ai/stable-diffusion/v1-5")
        
        # Check that an empty dict is returned on error
        assert result == {}
