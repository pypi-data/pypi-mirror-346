import json
import llm
import os
import pytest
from pydantic import BaseModel
from unittest.mock import patch, AsyncMock, MagicMock

# Import fixtures for sample responses
from .fixtures.responses import (
    MODELS_RESPONSE,
    MODEL_SCHEMA_RESPONSE,
    IMAGE_GENERATION_RESPONSE,
    VIDEO_GENERATION_RESPONSE,
    SPEECH_TO_TEXT_RESPONSE,
    TEXT_TO_SPEECH_RESPONSE,
    QUEUE_RESULT_RESPONSE
)

# Import functions to test directly from llm_fal
from llm_fal import (
    get_all_models, 
    get_model_category, 
    get_models_by_category,
    get_model_schema
)

# Sample image data for testing
TINY_PNG = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\xa6\x00\x00\x01\x1a"
    b"\x02\x03\x00\x00\x00\xe6\x99\xc4^\x00\x00\x00\tPLTE\xff\xff\xff"
    b"\x00\xff\x00\xfe\x01\x00\x12t\x01J\x00\x00\x00GIDATx\xda\xed\xd81\x11"
    b"\x000\x08\xc0\xc0.]\\\xea\\\xaf&Q\\\x89\x04V\\\xe0>\\\xf3+\\\xc8\\\x91Z\\\xf4\\\xa2\x08EQ\\\x14E"
    b"Q\\\x14EQ\\\x14EQ\\\xd4B\\\x91$I3\\\xbb\\\xbf\x08EQ\\\x14EQ\\\x14EQ\\\x14E\\\xd1\\\xa5"
    b"\\\xd4\\\x17\\\x91\\\xc6\\\x95\x05\\\x15\x0f\\\x9f\\\xc5\\\t\\\x9f\\\xa4\\\x00\\\x00\\\x00\\\x00IEND\\\xaeB`"
    b"\\\x82"
)

FAL_API_KEY = os.environ.get("PYTEST_FAL_API_KEY", None) or "fal-..."


@pytest.mark.vcr
def test_text_prompt():
    """Test basic text prompt with fal.ai model."""
    model = llm.get_model("fal-ai/text-generation/llm")
    model.key = model.key or FAL_API_KEY
    
    # Mock the fal_client.run_async method
    with patch('fal_client.run_async') as mock_run:
        # Configure mock to return a text response
        mock_run.return_value = {"data": {"text": "This is a sample response from a fal.ai text model."}}
        
        # Execute the prompt
        response = model.prompt("Generate a short description of fal.ai")
        
        # Verify response
        assert str(response) == "This is a sample response from a fal.ai text model."
        mock_run.assert_called_once()


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_async_text_prompt():
    """Test async text prompt with fal.ai model."""
    model = llm.get_async_model("fal-ai/text-generation/llm")
    model.key = model.key or FAL_API_KEY
    
    # Mock the fal_client.run_async method
    with patch('fal_client.run_async') as mock_run:
        mock_run.return_value = {"data": {"text": "This is an async response from fal.ai."}}
        
        # Create conversation and send prompt
        conversation = model.conversation()
        response = await conversation.prompt("Tell me about fal.ai")
        
        # Verify response
        assert await response.text() == "This is an async response from fal.ai."
        mock_run.assert_called_once()
        
        # Try a follow-up prompt
        mock_run.return_value = {"data": {"text": "Fal.ai provides AI services through APIs."}}
        response2 = await conversation.prompt("What services does it offer?")
        
        # Verify response
        assert await response2.text() == "Fal.ai provides AI services through APIs."
        assert mock_run.call_count == 2


@pytest.mark.vcr
def test_image_prompt():
    """Test image generation prompt with fal.ai model."""
    model = llm.get_model("fal-ai/stable-diffusion/v1-5")
    model.key = model.key or FAL_API_KEY
    
    # Mock the fal_client.run_async method
    with patch('fal_client.run_async') as mock_run:
        # Configure mock to return an image URL response
        mock_run.return_value = IMAGE_GENERATION_RESPONSE
        
        # Execute the prompt
        response = model.prompt("A beautiful sunset over mountains")
        
        # Verify response
        image_url = IMAGE_GENERATION_RESPONSE["images"][0]["url"]
        assert str(response) == image_url
        mock_run.assert_called_once()
        
        # Verify response JSON is stored
        response.response_json = IMAGE_GENERATION_RESPONSE


@pytest.mark.vcr
def test_image_with_parameters():
    """Test image generation with custom parameters."""
    model = llm.get_model("fal-ai/stable-diffusion/v1-5")
    model.key = model.key or FAL_API_KEY
    
    # Mock the _build_request_data method to capture parameters
    with patch('llm_fal.FalModel._build_request_data') as mock_build_data:
        # Return a basic request data
        mock_build_data.return_value = {"prompt": "Mountains"}
        
        # Mock the fal_client.run_async to return a simple response
        with patch('fal_client.run_async') as mock_run:
            mock_run.return_value = {"images": [{"url": "https://example.com/image.png"}]}
            
            # Execute prompt with parameters
            options = model.Options(
                width=768,
                height=768,
                steps=50,
                prompt_strength=8.0,
                seed=42
            )
            model.prompt("Mountains", options=options)
            
            # Verify parameters were passed correctly
            mock_build_data.assert_called_once()
            args, kwargs = mock_build_data.call_args
            
            # Check that prompt object includes our options
            prompt_obj = args[0]
            assert prompt_obj.options.width == 768
            assert prompt_obj.options.height == 768
            assert prompt_obj.options.steps == 50
            assert prompt_obj.options.prompt_strength == 8.0
            assert prompt_obj.options.seed == 42


class Pet(BaseModel):
    """Schema for testing structured output."""
    name: str
    species: str
    description: str


@pytest.mark.vcr
def test_schema_prompt():
    """Test structured output with schema."""
    model = llm.get_model("fal-ai/text-generation/llm")
    model.key = model.key or FAL_API_KEY
    
    # Mock the fal_client.run_async method
    with patch('fal_client.run_async') as mock_run:
        # Configure mock to yield a JSON response
        pet_json = json.dumps({
            "name": "Whiskers",
            "species": "Cat",
            "description": "A fluffy orange tabby with green eyes."
        })
        mock_run.return_value = {"data": {"text": pet_json}}
        
        # Execute the prompt with schema
        response = model.prompt("Describe a pet", schema=Pet)
        
        # Parse the JSON response into the Pet model
        pet = json.loads(response.text())
        
        # Verify response
        assert pet["name"] == "Whiskers"
        assert pet["species"] == "Cat"
        assert pet["description"] == "A fluffy orange tabby with green eyes."
        mock_run.assert_called_once()


@pytest.mark.vcr
def test_streaming_response():
    """Test streaming response handling."""
    model = llm.get_model("fal-ai/text-generation/llm")
    model.key = model.key or FAL_API_KEY
    
    # Create a mock streaming response for chat models
    async def mock_stream():
        stream_chunks = [
            MagicMock(delta=MagicMock(content="This ")),
            MagicMock(delta=MagicMock(content="is ")),
            MagicMock(delta=MagicMock(content="a ")),
            MagicMock(delta=MagicMock(content="streaming ")),
            MagicMock(delta=MagicMock(content="response ")),
            MagicMock(delta=MagicMock(content="from ")),
            MagicMock(delta=MagicMock(content="fal.ai."))
        ]
        for chunk in stream_chunks:
            yield chunk
    
    # Mock the fal_client.chat.stream method
    with patch('fal_client.chat.stream', return_value=mock_stream()):
        # Execute the prompt with streaming enabled
        response = model.prompt("Tell me a story", stream=True)
        
        # Verify the complete response was collected
        assert str(response) == "This is a streaming response from fal.ai."


@pytest.mark.vcr
def test_error_handling():
    """Test error handling in API calls."""
    model = llm.get_model("fal-ai/stable-diffusion/v1-5")
    model.key = model.key or FAL_API_KEY
    
    # Mock the fal_client.run_async method to raise an exception
    with patch('fal_client.run_async', side_effect=Exception("API Error")):
        # Execute the prompt and expect an exception
        with pytest.raises(Exception):
            model.prompt("This should fail")
            

@pytest.mark.vcr
def test_input_validation():
    """Test validation of input parameters."""
    model = llm.get_model("fal-ai/stable-diffusion/v1-5")
    
    # Test invalid temperature
    with pytest.raises(ValueError):
        options = model.Options(temperature=1.5)
        model.prompt("Test prompt", options=options)
    
    # Test invalid prompt strength
    with pytest.raises(ValueError):
        options = model.Options(prompt_strength=2.0)
        model.prompt("Test prompt", options=options)


@pytest.mark.vcr
def test_flux_image_generation():
    """Test image generation using the featured flux-pro model."""
    model = llm.get_model("fal-ai/flux-pro/v1.1-ultra")
    model.key = model.key or FAL_API_KEY
    
    # Mock the fal_client.run_async method
    with patch('fal_client.run_async') as mock_run:
        # Configure mock to return an image URL response
        mock_run.return_value = IMAGE_GENERATION_RESPONSE
        
        # Execute the prompt
        response = model.prompt("A futuristic cityscape with flying cars and neon lights")
        
        # Verify response
        image_url = IMAGE_GENERATION_RESPONSE["images"][0]["url"]
        assert str(response) == image_url
        mock_run.assert_called_once()
        
        # Verify proper arguments were passed
        call_args = mock_run.call_args
        assert "fal-ai/flux-pro/v1.1-ultra" in str(call_args)
        args, kwargs = call_args
        assert kwargs["arguments"]["prompt"] == "A futuristic cityscape with flying cars and neon lights"


@pytest.mark.vcr
def test_image_to_video_generation():
    """Test video generation from image using featured wan-pro model."""
    model = llm.get_model("fal-ai/wan-pro/image-to-video")
    model.key = model.key or FAL_API_KEY
    
    # Mock the fal_client.upload_file method
    with patch('fal_client.upload_file') as mock_upload:
        # Return a URL for the uploaded file
        mock_upload.return_value = "https://cdn.fal.ai/uploads/temp-image.png"
        
        # Mock the fal_client.run_async method
        with patch('fal_client.run_async') as mock_run:
            # Configure mock to return a video URL response
            mock_run.return_value = VIDEO_GENERATION_RESPONSE
            
            # Execute the prompt with attachment (image)
            options = model.Options(
                steps=30,
                seed=42
            )
            
            # Create an attachment to simulate an image
            attachment = llm.Attachment(content=TINY_PNG)
            response = model.prompt(
                "A person walking through a city street",
                options=options,
                attachments=[attachment]
            )
            
            # Verify response
            video_url = VIDEO_GENERATION_RESPONSE["videos"][0]["url"]
            assert str(response) == video_url
            
            # Verify file was uploaded
            mock_upload.assert_called_once()
            
            # Verify prompt and URL were passed to API
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert kwargs["arguments"]["prompt"] == "A person walking through a city street"
            assert "image_url" in kwargs["arguments"]
            assert kwargs["arguments"]["image_url"] == "https://cdn.fal.ai/uploads/temp-image.png"


@pytest.mark.vcr
def test_kling_video_model():
    """Test video generation using the featured kling-video model."""
    model = llm.get_model("fal-ai/kling-video/v2/master/image-to-video")
    model.key = model.key or FAL_API_KEY
    
    # Mock the fal_client.upload_file method
    with patch('fal_client.upload_file') as mock_upload:
        # Return a URL for the uploaded file
        mock_upload.return_value = "https://cdn.fal.ai/uploads/temp-image.png"
        
        # Mock the fal_client.run_async method
        with patch('fal_client.run_async') as mock_run:
            # Configure mock to return a video URL response
            mock_run.return_value = VIDEO_GENERATION_RESPONSE
            
            # Execute the prompt with attachment (image)
            options = model.Options(
                seed=12345
            )
            
            # Create an attachment to simulate an image
            attachment = llm.Attachment(content=TINY_PNG)
            response = model.prompt(
                "Smooth camera motion zooming in",
                options=options,
                attachments=[attachment]
            )
            
            # Verify response
            video_url = VIDEO_GENERATION_RESPONSE["videos"][0]["url"]
            assert str(response) == video_url
            
            # Verify file was uploaded
            mock_upload.assert_called_once()
            
            # Verify prompt and parameters were passed correctly
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert kwargs["arguments"]["prompt"] == "Smooth camera motion zooming in"
            assert kwargs["arguments"]["seed"] == 12345


@pytest.mark.vcr
def test_speech_to_text():
    """Test speech-to-text conversion using the featured playai TTS model."""
    model = llm.get_model("fal-ai/playai/tts/dialog")
    model.key = model.key or FAL_API_KEY
    
    # Mock the fal_client.run_async method
    with patch('fal_client.run_async') as mock_run:
        # Configure mock to yield text response from audio
        mock_run.return_value = SPEECH_TO_TEXT_RESPONSE
        
        # Execute the prompt with an audio file
        # In a real case, the audio would be sent as an attachment
        response = model.prompt(None)  # No prompt needed for speech-to-text
        
        # Verify response
        text_response = SPEECH_TO_TEXT_RESPONSE["data"]["text"]
        assert str(response) == text_response
        mock_run.assert_called_once()


@pytest.mark.vcr
def test_text_to_speech():
    """Test text-to-speech conversion using the PlayAI TTS model."""
    model = llm.get_model("fal-ai/playai/tts/dialog")
    model.key = model.key or FAL_API_KEY
    
    # Mock the fal_client.run_async method
    with patch('fal_client.run_async') as mock_run:
        # Configure mock to return an audio URL response
        mock_run.return_value = TEXT_TO_SPEECH_RESPONSE
        
        # Execute the prompt with TTS-specific options
        options = model.Options(
            voice="default",
            output_format="mp3"
        )
        
        response = model.prompt(
            "This is a test of the text to speech capabilities",
            options=options
        )
        
        # Verify response
        audio_url = TEXT_TO_SPEECH_RESPONSE["audio"]["url"]
        assert str(response) == audio_url
        mock_run.assert_called_once()
        
        # Verify proper parameters were passed
        args, kwargs = mock_run.call_args
        assert kwargs["arguments"]["input"] == "This is a test of the text to speech capabilities"
        assert kwargs["arguments"]["voice"] == "default"
        assert kwargs["arguments"]["outputFormat"] == "mp3"
