# llm-fal

[![PyPI](https://img.shields.io/pypi/v/llm-fal.svg)](https://pypi.org/project/llm-fal-ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Changelog](https://img.shields.io/github/v/release/nicobailon/llm-fal?include_prereleases&label=changelog)](https://github.com/nicobailon/llm-fal-ai/releases)
[![Tests](https://github.com/nicobailon/llm-fal-ai/actions/workflows/test.yml/badge.svg)](https://github.com/nicobailon/llm-fal-ai/actions/workflows/test.yml)

LLM CLI plugin for accessing fal.ai's generative AI models and services, including image generation, text processing, audio, and video models.

## Installation

Install this plugin in the same environment as [LLM](https://llm.datasette.io/).
```bash
llm install llm-fal
```

## Configuration

First, set [an API key for fal.ai](https://docs.fal.ai/authentication):
```bash
llm keys set fal
# Paste key here
```

You can also set the key in the environment variable `FAL_API_KEY`.

## Usage

Run `llm fal models` to list the available models, categorized by type (image, video, audio, text).

Run prompts with various models like this:
```bash
# Generate an image with standard parameters
llm -m fal-ai/fast-sdxl "A futuristic cityscape at sunset"

# Generate an image with custom parameters
llm -m fal-ai/lightning-sd "Astronaut on Mars" -o width 512 -o height 512 -o prompt_strength 7.5 -o steps 30

# Save generated image to file (using shell redirection)
llm -m fal-ai/fast-sdxl "Mountain landscape" > landscape.png

# Use text models if available
llm -m fal-ai/text-model "Write a short story about space travel"
```

### Image Attachments

For models that support image-to-video or other transformations, you can attach source images:

```bash
# Convert an image to video with WAN-Pro
llm -m fal-ai/wan-pro/image-to-video "Add smooth movement" -a source_image.jpg

# Convert an image to video with Kling
llm -m fal-ai/kling-video/v2/master/image-to-video "Add smooth camera movement" -a source_image.jpg -o duration 10 -o aspect_ratio "16:9"

# Process an image with a specific model
llm -m fal-ai/image-processor "Enhance quality" -a input.png
```

### Model Categories

The fal.ai plugin supports the following categories of models:

1. **Image Generation Models**: Stable Diffusion variants, FLUX.1, Lightning models, and other text-to-image models
   ```bash
   llm -m fal-ai/fast-sdxl "A cat wearing a space helmet"
   llm -m fal-ai/lightning-sd "Sunset over mountains" -o prompt_strength 8.0
   llm -m fal-ai/flux/dev "Portrait of a robot artist" -o width 1024 -o height 1024
   ```

2. **Video Generation Models**: Models for creating or manipulating video content
   ```bash
   # WAN Pro model
   llm -m fal-ai/wan-pro/image-to-video "Gentle camera movement" -a static_image.jpg
   
   # Kling Video model with additional options
   llm -m fal-ai/kling-video/v2/master/image-to-video "Smooth camera zoom" -a static_image.jpg -o duration 10 -o aspect_ratio "16:9" -o negative_prompt "blur, distortion" -o cfg_scale 0.8
   ```

3. **Audio Processing Models**: Audio generation or processing models
   ```bash
   # Text-to-speech conversion
   llm -m fal-ai/playai/tts/dialog "This is a test of the text to speech capabilities"
   
   # Text-to-speech with voice and format options
   llm -m fal-ai/playai/tts/dialog "Convert this text to speech" -o voice default -o output_format mp3
   ```

4. **Text-Based Models**: Any language models available on fal.ai's platform
   ```bash
   llm -m fal-ai/text-generation "Write a poem about technology"
   ```

5. **Custom Model Endpoints**: Support for user-deployed custom model endpoints
   ```bash
   llm -m fal-ai/custom-endpoint-id "Your custom model prompt"
   ```

## Model Options

The following options can be passed using `-o name value` on the CLI or as `keyword=value` arguments to the Python `model.prompt()` method:

- **max_tokens**: `int`
  
  The maximum number of tokens to generate (for text models)

- **temperature**: `float`
  
  Controls randomness in the output (0-1)

- **prompt_strength**: `float`
  
  Controls how much the output adheres to the prompt (for image models)

- **width**: `int`
  
  Width of generated image (for image models)

- **height**: `int`
  
  Height of generated image (for image models)

- **steps**: `int`
  
  Number of diffusion steps (for image models)

- **seed**: `int`
  
  Seed for reproducible generation

- **voice**: `string`
  
  Voice to use for text-to-speech models

- **output_format**: `string`
  
  Output format for audio (mp3, wav, etc.)
  
- **duration**: `int`
  
  Duration of the generated video in seconds (5 or 10, for Kling video model)
  
- **aspect_ratio**: `string`
  
  Aspect ratio of the generated video ("16:9", "9:16", or "1:1", for Kling video model)
  
- **negative_prompt**: `string`
  
  Negative prompt to specify unwanted elements in generation (for Kling video model)
  
- **cfg_scale**: `float`
  
  Controls adherence to prompt (0.0-1.0) for Kling video model

## Commands

The plugin provides the following CLI commands:

```bash
# List all available models categorized by type
llm fal models

# Check your API key
llm fal auth

# Set your API key
llm fal auth YOUR_API_KEY
```

## Python API Usage

You can also use this plugin programmatically:

```python
import llm

# Generate an image
response = llm.prompt(
    "A beautiful landscape with mountains and a lake",
    model="fal-ai/fast-sdxl",
    width=1024,
    height=768,
    prompt_strength=7.5
)

# Get the URL of the generated image
image_url = response.text()
print(f"Generated image: {image_url}")

# Generate a video from an image
import os
from pathlib import Path

# Path to your source image
image_path = Path("source_image.jpg")

# Ensure the path exists
if image_path.exists():
    video_response = llm.prompt(
        "Add smooth camera movement",
        model="fal-ai/kling-video/v2/master/image-to-video",
        duration=10,
        aspect_ratio="16:9",
        negative_prompt="blur, distortion",
        cfg_scale=0.7,
        attachments=[image_path]
    )
    
    # Get the URL of the generated video
    video_url = video_response.text()
    print(f"Generated video: {video_url}")

# Generate speech from text
tts_response = llm.prompt(
    "This is a text to speech test",
    model="fal-ai/playai/tts/dialog",
    voice="default",
    output_format="mp3"
)

# Get the URL of the audio file
audio_url = tts_response.text()
print(f"Generated audio: {audio_url}")

# Save the image using the LLM CLI utilities
# (For actual image saving, you would need to download the image using requests)
```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd llm-fal
python3 -m venv venv
source venv/bin/activate
```

Now install the plugin in development mode:
```bash
pip install -e '.[test,dev]'
```

## Testing

This project uses pytest for testing with pytest-vcr for recording and replaying API calls.

Run the tests:
```bash
pytest tests/
```

To run tests with coverage reporting:
```bash
pytest --cov=llm_fal tests/
```

When adding new tests, you can record new API interactions by setting your FAL API key and running:
```bash
PYTEST_FAL_API_KEY=your_api_key pytest tests/test_fal.py::test_name
```

The interactions will be recorded in the `tests/cassettes/` directory.

## Continuous Integration

This project uses GitHub Actions for continuous integration and deployment:

- **Testing**: All commits and pull requests are automatically tested against multiple Python versions
- **Publishing**: New releases are automatically published to PyPI when a new GitHub release is created

## Architecture

This plugin follows a simple, single-file architecture similar to other LLM CLI plugins. The core functionality is contained in:

- `llm_fal.py`: Main plugin file containing API client, model handling, and commands
- `pyproject.toml`: Project configuration
- `README.md`: Documentation 
- `LICENSE`: MIT License information

We intentionally kept the implementation minimal and streamlined, following the pattern of other successful LLM CLI plugins. This makes the code more maintainable and easier to understand while still providing all the core functionality needed.

## Credits

Developed for use with the [LLM](https://llm.datasette.io/) command line interface.
