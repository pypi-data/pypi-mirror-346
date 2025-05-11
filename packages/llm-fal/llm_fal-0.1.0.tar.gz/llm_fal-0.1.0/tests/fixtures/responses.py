"""
Recorded API responses for testing.

This module contains recorded responses from the fal.ai API that can be used
for testing without making actual API calls.
"""

# Models listing response
MODELS_RESPONSE = {
    "models": [
        {
            "id": "fal-ai/stable-diffusion/v1-5",
            "name": "Stable Diffusion v1.5",
            "description": "Stable Diffusion is a latent text-to-image diffusion model capable of generating photo-realistic images given text input.",
            "version": "1.5",
            "created_at": "2023-01-15T00:00:00Z",
            "updated_at": "2023-01-15T00:00:00Z"
        },
        {
            "id": "fal-ai/wan-pro/image-to-video",
            "name": "WAN Pro Image to Video",
            "description": "Convert images to videos with high quality and customizable effects.",
            "version": "1.0",
            "created_at": "2023-05-20T00:00:00Z",
            "updated_at": "2023-05-20T00:00:00Z"
        },
        {
            "id": "fal-ai/playai/tts/dialog",
            "name": "PlayAI Text to Speech",
            "description": "Convert text to natural-sounding speech with dialog capabilities.",
            "version": "2.1",
            "created_at": "2023-03-10T00:00:00Z",
            "updated_at": "2023-03-10T00:00:00Z"
        },
        {
            "id": "fal-ai/flux-pro/v1.1-ultra",
            "name": "Flux Pro Ultra",
            "description": "High-resolution image generation with advanced features and quality.",
            "version": "1.1",
            "created_at": "2023-06-15T00:00:00Z",
            "updated_at": "2023-06-15T00:00:00Z"
        },
        {
            "id": "fal-ai/flux-lora-fast-training",
            "name": "Flux LoRA Fast Training",
            "description": "Fast training for custom image generation models using LoRA technique.",
            "version": "1.0",
            "created_at": "2023-07-22T00:00:00Z",
            "updated_at": "2023-07-22T00:00:00Z"
        }
    ]
}

# Model schema response
MODEL_SCHEMA_RESPONSE = {
    "id": "fal-ai/stable-diffusion/v1-5",
    "name": "Stable Diffusion v1.5",
    "description": "Stable Diffusion is a latent text-to-image diffusion model capable of generating photo-realistic images given text input.",
    "version": "1.5",
    "parameters": {
        "prompt": {
            "type": "string",
            "description": "Text prompt for image generation",
            "required": True
        },
        "negative_prompt": {
            "type": "string",
            "description": "Text that the model should avoid in the generation",
            "required": False
        },
        "width": {
            "type": "integer",
            "description": "Image width in pixels",
            "default": 512,
            "minimum": 256,
            "maximum": 1024
        },
        "height": {
            "type": "integer",
            "description": "Image height in pixels",
            "default": 512,
            "minimum": 256,
            "maximum": 1024
        },
        "num_inference_steps": {
            "type": "integer",
            "description": "Number of denoising steps",
            "default": 30,
            "minimum": 1,
            "maximum": 100
        },
        "guidance_scale": {
            "type": "number",
            "description": "How closely the model should follow the prompt",
            "default": 7.5,
            "minimum": 1.0,
            "maximum": 20.0
        }
    }
}

# Image generation response
IMAGE_GENERATION_RESPONSE = {
    "images": [
        {
            "url": "https://cdn.fal.ai/generated/abcd1234-5678-90ef-ghij-klmnopqrstuv.png",
            "width": 512,
            "height": 512
        }
    ],
    "seed": 42,
    "metadata": {
        "prompt": "A futuristic cityscape at sunset",
        "model_id": "fal-ai/stable-diffusion/v1-5",
        "generation_time": 3.45
    }
}

# Video generation response
VIDEO_GENERATION_RESPONSE = {
    "videos": [
        {
            "url": "https://cdn.fal.ai/generated/video-abcd1234-5678-90ef-ghij-klmnopqrstuv.mp4",
            "width": 512, 
            "height": 512,
            "duration": 4.5
        }
    ],
    "seed": 12345,
    "metadata": {
        "prompt": "A person walking through a city street",
        "model_id": "fal-ai/wan-pro/image-to-video",
        "generation_time": 12.3,
        "input_image": "https://example.com/input-image.jpg"
    }
}

# Speech to text response
SPEECH_TO_TEXT_RESPONSE = {
    "data": {
        "text": "Hello, this is a sample transcription of speech to text using the fal.ai API. The model accurately converts spoken words into written text.",
        "detected_language": "en"
    },
    "metadata": {
        "model_id": "fal-ai/playai/tts/dialog",
        "audio_duration": 8.75,
        "processing_time": 2.1
    }
}

# Text to speech response
TEXT_TO_SPEECH_RESPONSE = {
    "url": "https://fal-ai-audio-uploads.s3.amazonaws.com/example-audio-12345.mp3",
    "audio": {
        "file_size": 123456,
        "duration": 5.2,
        "file_name": "example-audio-12345.mp3",
        "content_type": "audio/mpeg",
        "url": "https://fal-ai-audio-uploads.s3.amazonaws.com/example-audio-12345.mp3"
    }
}

# Queue creation response
QUEUE_CREATION_RESPONSE = {
    "queue_id": "queue_abcd1234",
    "status": "pending",
    "created_at": "2023-08-10T15:30:00Z",
    "model_id": "fal-ai/stable-diffusion/v1-5"
}

# Queue status response
QUEUE_STATUS_RESPONSE = {
    "queue_id": "queue_abcd1234",
    "status": "completed",
    "created_at": "2023-08-10T15:30:00Z",
    "completed_at": "2023-08-10T15:30:45Z",
    "model_id": "fal-ai/stable-diffusion/v1-5"
}

# Queue result response
QUEUE_RESULT_RESPONSE = {
    "queue_id": "queue_abcd1234",
    "status": "completed",
    "result": IMAGE_GENERATION_RESPONSE,
    "created_at": "2023-08-10T15:30:00Z",
    "completed_at": "2023-08-10T15:30:45Z",
    "model_id": "fal-ai/stable-diffusion/v1-5"
}

# File upload response
FILE_UPLOAD_RESPONSE = {
    "file_id": "file_abcd1234",
    "url": "https://cdn.fal.ai/uploads/abcd1234-5678-90ef-ghij-klmnopqrstuv.jpg",
    "content_type": "image/jpeg",
    "size": 1234567
}
