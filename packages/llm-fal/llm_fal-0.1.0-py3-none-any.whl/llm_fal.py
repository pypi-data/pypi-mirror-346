"""
Plugin for LLM CLI to access fal.ai generative AI models and services.

This plugin provides integration with fal.ai's generative AI models through
the LLM CLI interface, enabling users to access and use fal.ai's services
for generating images, audio, video, and text.
"""

import os
import json
import logging
import asyncio
import base64
from typing import Dict, Any, Optional, List, Union, Tuple
import llm
from pydantic import Field, field_validator, model_validator

# Import fal-client for API access
import fal_client

__version__ = "0.1.0"

# Set up logging
logger = logging.getLogger(__name__)

# Constants
PROVIDER_NAME = "fal"
KEY_ENV_VAR = "FAL_API_KEY"

# Model categories
MODEL_CATEGORIES = {
    "image": "Image Generation Models",
    "audio": "Audio Processing Models",
    "video": "Video Generation Models",
    "text": "Text-Based Models",
    "custom": "Custom Model Endpoints",
    "other": "Other Models"
}

# Cache for model metadata
_model_cache = {}


async def get_all_models() -> List[Dict[str, Any]]:
    """
    Fetch all available models from fal.ai API.
    
    Returns:
        List of model objects containing metadata.
    """
    if _model_cache.get("all_models"):
        return _model_cache["all_models"]
    
    try:
        # We need to use the synchronous version since list_models_async doesn't exist
        # Hard-code some models for now until an API for model discovery is available
        models = [
            # Image models
            {"id": "fal-ai/fast-sdxl", "name": "Fast SDXL", "description": "Faster version of Stable Diffusion XL"},
            {"id": "fal-ai/lightning-sd", "name": "Lightning SD", "description": "Ultra-fast Stable Diffusion model"},
            {"id": "fal-ai/flux-pro/v1.1-ultra", "name": "Flux Pro Ultra", "description": "High-resolution image generation with advanced features and quality"},
            {"id": "fal-ai/flux/dev", "name": "FLUX.1 Developer", "description": "FLUX.1 text-to-image model for developers"},
            {"id": "fal-ai/flux/schnell", "name": "FLUX.1 Schnell", "description": "Faster text-to-image generation with FLUX.1 model"},
            {"id": "fal-ai/esrgan", "name": "ESRGAN Upscaler", "description": "Enhanced image upscaling with ESRGAN"},
            
            # Video models
            {"id": "fal-ai/wan-pro/image-to-video", "name": "WAN Pro Image to Video", "description": "Convert still images to videos with high-quality motion"},
            {"id": "fal-ai/kling-video/v2/master/image-to-video", "name": "Kling Video", "description": "Advanced image to video conversion with sophisticated motion controls"},
            
            # Audio models
            {"id": "fal-ai/playai/tts/dialog", "name": "PlayAI TTS", "description": "Text to speech model with natural dialog capabilities"},
            
            # Text models
            {"id": "fal-ai/text-generation/llm", "name": "Text Generation", "description": "General purpose text generation model"}
        ]
        
        # Cache the results
        _model_cache["all_models"] = models
        return models
    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        return []


def get_model_category(model: Dict[str, Any]) -> str:
    """
    Determine the category of a model based on its metadata.
    
    Args:
        model: Model object with metadata
        
    Returns:
        Category string (image, video, audio, text, custom, or other)
    """
    model_id = model.get("id", "").lower()
    description = model.get("description", "").lower()
    name = model.get("name", "").lower()
    
    # Latest fal.ai models
    if any(id in model_id for id in ["flux-pro", "flux.1", "flux/dev", "flux/schnell"]):
        return "image"
    elif any(id in model_id for id in ["esrgan", "upscaler"]):
        return "image"
    elif any(id in model_id for id in ["recraft", "stable-diffusion", "fast-sdxl", "lightning-sd"]):
        return "image"
    elif any(id in model_id for id in ["kling-video", "wan-pro", "wan-i2v", "wan-effects", "veo2", "image-to-video"]):
        return "video"
    elif any(id in model_id for id in ["playai/tts", "whisper", "wizper", "speech-to-text", "voice"]):
        return "audio"
    
    # General categorization logic
    if any(kw in model_id for kw in ["sd", "stable-diffusion", "image", "img"]):
        return "image"
    elif any(kw in model_id for kw in ["video", "motion"]):
        return "video"
    elif any(kw in model_id for kw in ["audio", "speech", "voice", "tts"]):
        return "audio"
    elif any(kw in model_id for kw in ["text", "gpt", "llm", "language"]):
        return "text"
    elif "custom" in model_id:
        return "custom"
    
    # Fallback to category based on name or description
    if any(kw in name for kw in ["image", "picture", "photo"]):
        return "image"
    elif any(kw in name for kw in ["video", "motion", "animation"]):
        return "video"
    elif any(kw in name for kw in ["audio", "speech", "voice", "text to speech", "tts"]):
        return "audio"
    
    # Fallback to description
    if any(kw in description for kw in ["image", "picture", "photo"]):
        return "image"
    elif any(kw in description for kw in ["video", "motion", "animation"]):
        return "video"
    elif any(kw in description for kw in ["audio", "speech", "voice"]):
        return "audio"
    elif any(kw in description for kw in ["text", "language", "chat"]):
        return "text"
    
    return "other"


def get_models_by_category() -> Dict[str, List[Dict[str, Any]]]:
    """
    Group all available models by category.
    
    Returns:
        Dictionary mapping category names to lists of models.
    """
    # Use the hardcoded models - this avoids asyncio issues
    all_models = [
        # Image models
        {"id": "fal-ai/fast-sdxl", "name": "Fast SDXL", "description": "Faster version of Stable Diffusion XL"},
        {"id": "fal-ai/lightning-sd", "name": "Lightning SD", "description": "Ultra-fast Stable Diffusion model"},
        {"id": "fal-ai/flux-pro/v1.1-ultra", "name": "Flux Pro Ultra", "description": "High-resolution image generation with advanced features and quality"},
        {"id": "fal-ai/flu  x/dev", "name": "FLUX.1 Developer", "description": "FLUX.1 text-to-image model for developers"},
        {"id": "fal-ai/flux/schnell", "name": "FLUX.1 Schnell", "description": "Faster text-to-image generation with FLUX.1 model"},
        {"id": "fal-ai/esrgan", "name": "ESRGAN Upscaler", "description": "Enhanced image upscaling with ESRGAN"},
        
        # Video models
        {"id": "fal-ai/wan-pro/image-to-video", "name": "WAN Pro Image to Video", "description": "Convert still images to videos with high-quality motion"},
        {"id": "fal-ai/kling-video/v2/master/image-to-video", "name": "Kling Video", "description": "Advanced image to video conversion with sophisticated motion controls"},
        
        # Audio models
        {"id": "fal-ai/playai/tts/dialog", "name": "PlayAI TTS", "description": "Text to speech model with natural dialog capabilities"},
        
        # Text models
        {"id": "fal-ai/text-generation/llm", "name": "Text Generation", "description": "General purpose text generation model"}
    ]
    
    # Initialize result dictionary with empty lists for each category
    result = {category: [] for category in MODEL_CATEGORIES.keys()}
    
    # Categorize each model
    for model in all_models:
        category = get_model_category(model)
        result[category].append(model)
    
    return result


def search_models(query: str) -> List[Dict[str, Any]]:
    """
    Search for models by keyword in ID, name, or description.
    
    Args:
        query: Search keyword
        
    Returns:
        List of matching model objects.
    """
    # Use the hardcoded models directly - this avoids asyncio issues
    all_models = [
        # Image models
        {"id": "fal-ai/fast-sdxl", "name": "Fast SDXL", "description": "Faster version of Stable Diffusion XL"},
        {"id": "fal-ai/lightning-sd", "name": "Lightning SD", "description": "Ultra-fast Stable Diffusion model"},
        {"id": "fal-ai/flux-pro/v1.1-ultra", "name": "Flux Pro Ultra", "description": "High-resolution image generation with advanced features and quality"},
        {"id": "fal-ai/flux/dev", "name": "FLUX.1 Developer", "description": "FLUX.1 text-to-image model for developers"},
        {"id": "fal-ai/flux/schnell", "name": "FLUX.1 Schnell", "description": "Faster text-to-image generation with FLUX.1 model"},
        {"id": "fal-ai/esrgan", "name": "ESRGAN Upscaler", "description": "Enhanced image upscaling with ESRGAN"},
        
        # Video models
        {"id": "fal-ai/wan-pro/image-to-video", "name": "WAN Pro Image to Video", "description": "Convert still images to videos with high-quality motion"},
        {"id": "fal-ai/kling-video/v2/master/image-to-video", "name": "Kling Video", "description": "Advanced image to video conversion with sophisticated motion controls"},
        
        # Audio models
        {"id": "fal-ai/playai/tts/dialog", "name": "PlayAI TTS", "description": "Text to speech model with natural dialog capabilities"},
        
        # Text models
        {"id": "fal-ai/text-generation/llm", "name": "Text Generation", "description": "General purpose text generation model"}
    ]
    
    # Convert query to lowercase for case-insensitive search
    query = query.lower()
    
    # Filter models by query
    return [
        model for model in all_models
        if (
            query in model.get("id", "").lower() or
            query in model.get("name", "").lower() or
            query in model.get("description", "").lower()
        )
    ]


def get_model_schema_sync(model_id: str) -> Dict[str, Any]:
    """
    Simplified version that returns an empty schema - the actual method doesn't exist in fal_client.
    
    Args:
        model_id: The ID of the model to get schema for
        
    Returns:
        Empty schema object.
    """
    # Just return an empty dict as schema since fal_client doesn't have get_model_schema
    return {}

async def get_model_schema(model_id: str) -> Dict[str, Any]:
    """
    Simplified version that returns an empty schema - the actual method doesn't exist in fal_client.
    
    Args:
        model_id: The ID of the model to get schema for
        
    Returns:
        Empty schema object.
    """
    # Just return an empty dict as schema since fal_client doesn't have get_model_schema
    return {}


def get_api_key(key: Optional[str] = None) -> Optional[str]:
    """
    Get the fal.ai API key.
    
    Checks sources in the following order:
    1. Provided key parameter
    2. Environment variable FAL_API_KEY
    3. LLM CLI key store
    
    Args:
        key: Optional API key provided directly
        
    Returns:
        The API key as a string or None if not set in any location.
    """
    if key:
        return key
        
    # Check environment variable
    env_key = os.environ.get(KEY_ENV_VAR)
    if env_key:
        return env_key
    
    # Finally check LLM CLI key store
    try:
        cli_key = llm.get_key(PROVIDER_NAME)
        if cli_key:
            return cli_key
    except Exception as e:
        logger.debug(f"Error retrieving key from LLM CLI: {e}")
    
    return None


class FalOptions(llm.Options):
    """Options for fal.ai models."""
    
    max_tokens: Optional[int] = Field(
        description="The maximum number of tokens to generate (for text models)",
        default=None,
    )
    
    temperature: Optional[float] = Field(
        description="Controls randomness in the output (0-1)",
        default=None,
    )
    
    prompt_strength: Optional[float] = Field(
        description="Controls how much the output adheres to the prompt (for image models)",
        default=None,
    )
    
    width: Optional[int] = Field(
        description="Width of generated image (for image models)",
        default=None,
    )
    
    height: Optional[int] = Field(
        description="Height of generated image (for image models)",
        default=None,
    )
    
    steps: Optional[int] = Field(
        description="Number of diffusion steps (for image models)",
        default=None,
    )
    
    seed: Optional[int] = Field(
        description="Seed for reproducible generation",
        default=None,
    )
    
    voice: Optional[str] = Field(
        description="Voice to use for text-to-speech models",
        default=None,
    )
    
    output_format: Optional[str] = Field(
        description="Output format for audio (mp3, wav, etc.)",
        default=None,
    )
    
    # Additional parameters for Kling video model
    duration: Optional[int] = Field(
        description="Duration of the generated video in seconds (for video models like Kling)",
        default=None,
    )
    
    aspect_ratio: Optional[str] = Field(
        description="Aspect ratio of the video (for video models like Kling, e.g. '16:9', '9:16', '1:1')",
        default=None,
    )
    
    negative_prompt: Optional[str] = Field(
        description="Negative prompt to specify unwanted elements in the generation",
        default=None,
    )
    
    cfg_scale: Optional[float] = Field(
        description="Controls adherence to prompt (0.0-1.0) for certain video models",
        default=None,
    )
    
    @field_validator("temperature")
    @classmethod
    def validate_temperature(cls, temperature):
        if temperature is not None and not (0.0 <= temperature <= 1.0):
            raise ValueError("temperature must be in range 0.0-1.0")
        return temperature
    
    @field_validator("prompt_strength")
    @classmethod
    def validate_prompt_strength(cls, prompt_strength):
        if prompt_strength is not None and not (0.0 <= prompt_strength <= 1.0):
            raise ValueError("prompt_strength must be in range 0.0-1.0")
        return prompt_strength
        
    @field_validator("cfg_scale")
    @classmethod
    def validate_cfg_scale(cls, cfg_scale):
        if cfg_scale is not None and not (0.0 <= cfg_scale <= 1.0):
            raise ValueError("cfg_scale must be in range 0.0-1.0")
        return cfg_scale
        
    @field_validator("duration")
    @classmethod
    def validate_duration(cls, duration):
        if duration is not None and duration not in [5, 10]:
            raise ValueError("duration must be either 5 or 10 seconds for Kling video")
        return duration
        
    @field_validator("aspect_ratio")
    @classmethod
    def validate_aspect_ratio(cls, aspect_ratio):
        if aspect_ratio is not None and aspect_ratio not in ["16:9", "9:16", "1:1"]:
            raise ValueError("aspect_ratio must be one of: '16:9', '9:16', '1:1'")
        return aspect_ratio


class FalModel(llm.KeyModel):
    """Model implementation for fal.ai."""
    
    needs_key = PROVIDER_NAME
    key_env_var = KEY_ENV_VAR
    can_stream = True
    
    class Options(FalOptions): ...
    
    def __init__(self, model_id: str, model_info: Optional[Dict[str, Any]] = None):
        """Initialize a new fal.ai model."""
        self.fal_model_id = model_id
        self.model_id = model_id  # Use the original model ID directly for registration with LLM
        self.model_info = model_info or {}
        self.category = get_model_category(model_info or {"id": model_id})
        
        # Initialize schema with an empty dict
        self.schema = {}
        
        # Add attachment_types based on model category
        if self.category in ["image", "video"]:
            self.attachment_types = ["image/jpeg", "image/png", "image/webp", "image/gif"]
    
    # Schema is now initialized directly in __init__
    
    def execute(self, prompt, stream, response, conversation, key):
        """Execute the model with the given prompt."""
        api_key = self.get_key(key)
        if not api_key:
            raise llm.MissingKeyError(f"API key required for {self.model_id}. Use 'llm keys set fal' or set {KEY_ENV_VAR}.")
        
        # Configure fal_client with the API key
        os.environ["FAL_KEY"] = api_key
        
        # Create a new event loop for each request
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # For non-streaming responses, we need to collect all the chunks
            if not stream:
                # Run the async generator and collect all yielded items
                async def run_and_collect():
                    result = []
                    async for chunk in self._execute_async(prompt, stream, response, conversation):
                        result.append(chunk)
                    return result
                
                # Run the collector and return the results
                try:
                    return loop.run_until_complete(run_and_collect())
                finally:
                    # Ensure the loop is closed to prevent resource leaks
                    loop.close()
            else:
                # For streaming, we need to create a stream-like iterable
                # Use a custom iterable that yields chunks from the async generator
                # This is important because the LLM CLI expects a synchronous iterable
                class AsyncIteratorWrapper:
                    def __init__(self, async_gen, loop):
                        self.async_gen = async_gen
                        self.loop = loop
                        self.queue = asyncio.Queue()
                        self.sentinel = object()
                        self.loop.create_task(self._fill_queue())
                    
                    async def _fill_queue(self):
                        try:
                            async for item in self.async_gen:
                                await self.queue.put(item)
                            await self.queue.put(self.sentinel)
                        except Exception as e:
                            await self.queue.put(f"Error: {str(e)}")
                            await self.queue.put(self.sentinel)
                    
                    def __iter__(self):
                        return self
                    
                    def __next__(self):
                        if self.loop.is_closed():
                            raise StopIteration
                        
                        try:
                            next_item = self.loop.run_until_complete(self.queue.get())
                            if next_item is self.sentinel:
                                # Clean up when we're done
                                self.loop.close()
                                raise StopIteration
                            return next_item
                        except (StopIteration, RuntimeError):
                            # Ensure we clean up on error too
                            if not self.loop.is_closed():
                                self.loop.close()
                            raise StopIteration
                
                return AsyncIteratorWrapper(self._execute_async(prompt, stream, response, conversation), loop)
        except Exception as e:
            logger.error(f"Error executing model: {e}")
            # Clean up the event loop on error
            loop.close()
            raise
    
    async def _execute_async(self, prompt, stream, response, conversation):
        """Async implementation of model execution."""
        # Build request data based on model category - using synchronous method
        data = self._build_request_data(prompt)
        
        # Log data being sent at debug level only
        logger.debug(f"Sending data to model {self.fal_model_id}: {data}")
        
        if stream:
            # Handle streaming responses
            async for chunk in self._stream_response(self.fal_model_id, data, self.category):
                yield chunk
        else:
            # Handle non-streaming responses
            try:
                result = await fal_client.run_async(self.fal_model_id, arguments=data)
                
                # Process the response based on model category
                output = self._process_response(result, self.category)
                # Yield the single result for non-streaming case
                yield output
                
                # Store the raw response for future reference
                if response:
                    response.response_json = result
            except Exception as e:
                logger.error(f"Error executing model {self.fal_model_id}: {e}")
                # Yield the error message so it's visible
                yield f"Error: {str(e)}"
                raise
    
    def _build_request_data(self, prompt) -> Dict[str, Any]:
        """Build request data for the API based on prompt and options."""
        data = {}
        
        # Add prompt if provided, with model-specific handling
        if prompt.prompt is not None:
            # Special handling for PlayAI TTS model
            if "playai/tts" in self.fal_model_id.lower():
                data["input"] = prompt.prompt
            else:
                data["prompt"] = prompt.prompt
        
        # Add common options
        if prompt.options.seed is not None:
            data["seed"] = prompt.options.seed
            
        if prompt.options.temperature is not None:
            data["temperature"] = prompt.options.temperature
        
        # Add category-specific options
        if self.category == "image":
            if prompt.options.width is not None:
                data["width"] = prompt.options.width
                
            if prompt.options.height is not None:
                data["height"] = prompt.options.height
                
            if prompt.options.steps is not None:
                data["num_inference_steps"] = prompt.options.steps
                
            if prompt.options.prompt_strength is not None:
                data["guidance_scale"] = prompt.options.prompt_strength
        
        elif self.category == "text":
            if prompt.options.max_tokens is not None:
                data["max_tokens"] = prompt.options.max_tokens
                
        elif self.category == "video":
            if prompt.options.steps is not None:
                data["num_inference_steps"] = prompt.options.steps
                
            # Video-specific parameters
            if "kling" in self.fal_model_id.lower():
                # Kling video model specific parameters
                if prompt.options.duration is not None:
                    data["duration"] = str(prompt.options.duration)  # Kling requires duration as string
                
                if prompt.options.aspect_ratio is not None:
                    data["aspect_ratio"] = prompt.options.aspect_ratio
                    
                if prompt.options.negative_prompt is not None:
                    data["negative_prompt"] = prompt.options.negative_prompt
                    
                if prompt.options.cfg_scale is not None:
                    data["cfg_scale"] = prompt.options.cfg_scale
                    
        elif self.category == "audio":
            # Add specific parameters for TTS models
            if "playai/tts" in self.fal_model_id.lower():
                # Add voice parameter if provided or use default
                if prompt.options.voice is not None:
                    data["voice"] = prompt.options.voice
                elif "voice" not in data:
                    data["voice"] = "default"
                
                # Add output format if provided or use default
                if prompt.options.output_format is not None:
                    data["outputFormat"] = prompt.options.output_format
                elif "outputFormat" not in data:
                    data["outputFormat"] = "mp3"
        
        # Handle attachments if any
        if prompt.attachments:
            logger.debug(f"Found {len(prompt.attachments)} attachments")
            for i, attachment in enumerate(prompt.attachments):
                logger.debug(f"Attachment {i+1} has attributes: {dir(attachment)}")
                if hasattr(attachment, "content"):
                    if attachment.content:
                        logger.debug(f"Attachment has content with size {len(attachment.content)} bytes")
                    else:
                        logger.debug(f"Attachment has content attribute but it's empty")
                if hasattr(attachment, "path"):
                    logger.debug(f"Attachment has path: {attachment.path}")
                if hasattr(attachment, "url"):
                    logger.debug(f"Attachment has URL: {attachment.url}")
                
                # Process the attachment based on what data is available
                file_content = None
                
                # Try to get content from the content attribute
                if hasattr(attachment, "content") and attachment.content:
                    file_content = attachment.content
                    logger.debug(f"Using content from attachment.content")
                # If content is not available, try to read from the file path
                elif hasattr(attachment, "path") and attachment.path:
                    try:
                        with open(attachment.path, "rb") as f:
                            file_content = f.read()
                            logger.debug(f"Read {len(file_content)} bytes from file: {attachment.path}")
                    except Exception as e:
                        logger.error(f"Error reading file: {e}")
                        raise
                # If neither content nor path works, try to use the URL
                elif hasattr(attachment, "url") and attachment.url:
                    # URL attachments are handled below
                    logger.debug(f"Will use URL: {attachment.url}")
                
                # Now process the attachment based on what we found
                if file_content and (self.category == "image" or self.category == "video"):
                    # Upload the image content
                    # Write to a temporary file first
                    import tempfile
                    import os
                    
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
                        temp.write(file_content)
                        temp_path = temp.name
                        
                        try:
                            # Use upload_file (not async) to avoid awaitable issues
                            logger.debug(f"Uploading image from {temp_path}")
                            upload_url = fal_client.upload_file(temp_path)
                            logger.debug(f"Upload successful, URL: {upload_url}")
                            # For video models like wan-pro/image-to-video, ensure image_url is set
                            data["image_url"] = upload_url
                            logger.debug(f"Set image_url in data to {upload_url}")
                        except Exception as e:
                            logger.error(f"Error uploading file: {e}")
                            raise
                        finally:
                            # Clean up the temporary file
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
                
                elif self.category == "audio":
                        # Similar approach for audio files
                        import tempfile
                        import os
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
                            temp.write(attachment.content)
                            temp_path = temp.name
                        
                        try:
                            # Use upload_file (not async) to avoid awaitable issues
                            upload_url = fal_client.upload_file(temp_path)
                            data["audio_url"] = upload_url
                        finally:
                            # Clean up the temporary file
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
                
                # Or use an existing URL direct from attachment
                elif hasattr(attachment, "url") and attachment.url:
                    logger.debug(f"Using URL from attachment: {attachment.url}")
                    if self.category == "image" or self.category == "video":
                        data["image_url"] = attachment.url
                        logger.debug(f"Set image_url in data to URL: {attachment.url}")
                    elif self.category == "audio":
                        data["audio_url"] = attachment.url
        
        # Return the data immediately
        return data
    
    async def _stream_response(self, model_id, data, category):
        """Process streaming response based on model category."""
        try:
            # For text models, use the streaming API
            if category == "text":
                from fal_client import chat  # or appropriate streaming endpoint
                
                async for chunk in chat.stream(
                    model=model_id,
                    messages=[{"role": "user", "content": data.get("prompt", "")}],
                    temperature=data.get("temperature", 0.7),
                    max_tokens=data.get("max_tokens", 1000)
                ):
                    if chunk.delta and chunk.delta.content:
                        yield chunk.delta.content
            else:
                # For non-text models, we might not have proper streaming
                # So just yield the final result
                result = await fal_client.run_async(model_id, arguments=data)
                output = self._process_response(result, category)
                yield output
        except Exception as e:
            logger.error(f"Error in streaming response: {e}")
            # Yield the error message if we can't stream properly
            yield f"Error: {str(e)}"
    
    def _process_response(self, result, category):
        """Process the API response based on model category."""
        # Log the entire response at debug level
        logger.debug(f"Raw API response: {result}")
        
        if category == "image":
            # Extract image URL from response
            if "images" in result and result["images"]:
                logger.debug(f"Found images in response: {result['images']}")
                return result["images"][0].get("url", str(result))
            return str(result)
        
        elif category == "text":
            # Extract text from response
            if "data" in result and "text" in result["data"]:
                logger.debug(f"Found text data in response")
                return result["data"]["text"]
            return str(result)
        
        elif category == "video":
            logger.debug(f"Processing video response")
            # Extract video URL from response
            
            # Standard format with videos array
            if "videos" in result and result["videos"]:
                logger.debug(f"Found videos in response: {result['videos']}")
                url = result["videos"][0].get("url", str(result))
                logger.debug(f"Extracted video URL: {url}")
                return url
                
            # WAN-specific response format
            elif "output" in result:
                logger.debug(f"Found output field in response: {result['output']}")
                if isinstance(result["output"], dict) and "video" in result["output"]:
                    url = result["output"]["video"]
                    logger.debug(f"Extracted video URL from output.video: {url}")
                    return url
                    
            # Kling video response format
            elif "video" in result and isinstance(result["video"], dict) and "url" in result["video"]:
                url = result["video"]["url"]
                logger.debug(f"Extracted video URL from Kling video.url format: {url}")
                return url
                
            # Alternative simple video response format 
            elif "video" in result and isinstance(result["video"], str):
                url = result["video"]
                logger.debug(f"Extracted video URL from direct video field: {url}")
                return url
                
            # If no standard format matches, return the raw result
            return str(result)
        
        elif category == "audio":
            # Multiple possible response formats for audio
            # 1. Speech-to-text response
            if "data" in result and "text" in result["data"]:
                return result["data"]["text"]
            
            # 2. Text-to-speech response with audio URL - PlayAI TTS format
            if "audio" in result:
                logger.debug(f"Found audio in response: {result['audio']}")
                if isinstance(result["audio"], dict) and "url" in result["audio"]:
                    return result["audio"]["url"]
                elif isinstance(result["audio"], str):
                    return result["audio"]
            
            # 3. Alternative TTS response format
            if "url" in result:
                logger.debug(f"Found direct URL in response: {result['url']}")
                return result["url"]
                    
            # 4. Alternative format with media field
            if "media" in result and "url" in result["media"]:
                logger.debug(f"Found media.url in response: {result['media']['url']}")
                return result["media"]["url"]
            
            # Log the raw result for debugging purposes
            logger.debug(f"Could not extract audio URL from response: {result}")
            return str(result)
        
        # Default fallback
        return str(result)


@llm.hookimpl
def register_models(register):
    """Register models with LLM CLI."""
    # Hard-code models directly instead of trying to fetch them
    # This avoids asyncio issues and prevents errors at registration time
    example_models = [
        # Image models
        {"id": "fal-ai/fast-sdxl", "name": "Fast SDXL", "description": "Faster version of Stable Diffusion XL"},
        {"id": "fal-ai/lightning-sd", "name": "Lightning SD", "description": "Ultra-fast Stable Diffusion model"},
        {"id": "fal-ai/flux-pro/v1.1-ultra", "name": "Flux Pro Ultra", "description": "High-resolution image generation with advanced features and quality"},
        {"id": "fal-ai/flux/dev", "name": "FLUX.1 Developer", "description": "FLUX.1 text-to-image model for developers"},
        {"id": "fal-ai/flux/schnell", "name": "FLUX.1 Schnell", "description": "Faster text-to-image generation with FLUX.1 model"},
        {"id": "fal-ai/esrgan", "name": "ESRGAN Upscaler", "description": "Enhanced image upscaling with ESRGAN"},
        
        # Video models
        {"id": "fal-ai/wan-pro/image-to-video", "name": "WAN Pro Image to Video", "description": "Convert still images to videos with high-quality motion"},
        {"id": "fal-ai/kling-video/v2/master/image-to-video", "name": "Kling Video", "description": "Advanced image to video conversion with sophisticated motion controls"},
        
        # Audio models
        {"id": "fal-ai/playai/tts/dialog", "name": "PlayAI TTS", "description": "Text to speech model with natural dialog capabilities"},
        
        # Text models
        {"id": "fal-ai/text-generation/llm", "name": "Text Generation", "description": "General purpose text generation model"}
    ]
    
    # Register each model
    for model in example_models:
        model_id = model.get("id")
        register(FalModel(model_id, model))


@llm.hookimpl
def register_commands(cli):
    """Register commands with LLM CLI.
    
    The parameter should be 'cli' not 'add_command' in newer versions of LLM CLI.
    """
    import click
    
    @cli.group(name="fal")
    def fal_command_group():
        """Commands for interacting with fal.ai services."""
        pass
    
    @fal_command_group.command(name="auth")
    @click.argument("api_key", required=False)
    def auth_command(api_key=None):
        """Set or check the fal.ai API key."""
        if api_key:
            # Set the API key
            llm.set_key(PROVIDER_NAME, api_key)
            click.echo(f"✅ API key set for {PROVIDER_NAME}")
        else:
            # Check if API key is set
            key = get_api_key()
            if key:
                masked_key = f"{key[:4]}...{key[-4:]}" if len(key) > 8 else "****"
                click.echo(f"API key is set: {masked_key}")
            else:
                click.echo(f"No API key set for {PROVIDER_NAME}")
                click.echo(f"Set it with: llm fal auth YOUR_API_KEY")
                click.echo(f"Or use environment variable: {KEY_ENV_VAR}")
    
    @fal_command_group.command(name="models")
    def list_models_command():
        """List available fal.ai models."""
        # Get models by category
        models_by_category = get_models_by_category()
        
        # Display models by category
        for category, models in models_by_category.items():
            if models:
                click.echo(f"\n{MODEL_CATEGORIES.get(category, category)} ({len(models)}):")
                click.echo("-" * 80)
                
                for model in models:
                    model_id = model.get("id", "")
                    name = model.get("name", model_id)
                    description = model.get("description", "No description available")
                    
                    click.echo(f"- {model_id}: {name}")
                    click.echo(f"  {description}\n")


@llm.hookimpl
def process_response(response):
    """Process responses from fal.ai models."""
    if response and response.model and "fal-ai/" in response.model:
        # Handle image/media URLs in responses
        content = response.text()
        logger.debug(f"Processing response: {content}")
        
        # Check if the response contains a URL to media
        if content.startswith("http") and any(ext in content for ext in [".png", ".jpg", ".mp4", ".wav"]):
            # This is a media URL
            response.set_extra("media_url", content)
            
            # For terminal output, just return the URL with a message
            if any(ext in content for ext in [".mp4", ".mov", ".avi"]):
                media_type = "video"
            elif any(ext in content for ext in [".png", ".jpg", ".jpeg", ".webp"]):
                media_type = "image"
            else:
                media_type = "media"
                
            return f"Generated {media_type} available at:\n{content}"
        
        # Sometimes the API returns full JSON response as a string
        if content.startswith("{") and content.endswith("}"):
            try:
                data = json.loads(content)
                # Check if it's a video response
                if "videos" in data and data["videos"]:
                    url = data["videos"][0].get("url", "")
                    if url:
                        response.set_extra("media_url", url)
                        return f"Generated video available at:\n{url}"
                # Check for WAN format
                if "output" in data and isinstance(data["output"], dict) and "video" in data["output"]:
                    url = data["output"]["video"]
                    response.set_extra("media_url", url)
                    return f"Generated video available at:\n{url}"
                # Check for Kling format
                if "video" in data:
                    if isinstance(data["video"], dict) and "url" in data["video"]:
                        url = data["video"]["url"]
                        response.set_extra("media_url", url)
                        return f"Generated video available at:\n{url}"
                    elif isinstance(data["video"], str) and data["video"].startswith("http"):
                        url = data["video"]
                        response.set_extra("media_url", url)
                        return f"Generated video available at:\n{url}"
            except json.JSONDecodeError:
                pass
    
    # Return None to let other processors handle it
    return None
