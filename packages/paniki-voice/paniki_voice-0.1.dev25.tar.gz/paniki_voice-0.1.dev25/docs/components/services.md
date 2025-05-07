# AI Services Integration

## Overview

Paniki supports integration with various AI services for:
- Language Models (LLM)
- Speech-to-Text (STT)
- Text-to-Speech (TTS)
- Image Processing
- Video Processing

## Language Models (LLM)

### OpenAI Integration

```python
from paniki.services.openai import OpenAILLMService

llm = OpenAILLMService(
    api_key="your-api-key",
    model="gpt-4-turbo-preview"
)
```

### Google Gemini Integration

```python
from paniki.services.gemini_multimodal_live.gemini import GeminiMultimodalLiveLLMService

llm = GeminiMultimodalLiveLLMService(
    api_key="your-api-key",
    transcribe_user_audio=True
)
```

### Anthropic Integration

```python
from paniki.services.anthropic import AnthropicLLMService

llm = AnthropicLLMService(
    api_key="your-api-key"
)
```

## Speech-to-Text (STT)

### Whisper Integration

```python
from paniki.services.whisper import WhisperSTTService

stt = WhisperSTTService()
```

### Google Speech Integration

```python
from paniki.services.google import GoogleSTTService

stt = GoogleSTTService(
    api_key="your-api-key"
)
```

## Text-to-Speech (TTS)

### ElevenLabs Integration

```python
from paniki.services.elevenlabs import ElevenLabsTTSService

tts = ElevenLabsTTSService(
    api_key="your-api-key",
    voice_id="your-voice-id"
)
```

### AWS Polly Integration

```python
from paniki.services.aws import AWSPollyTTSService

tts = AWSPollyTTSService(
    aws_access_key_id="your-access-key",
    aws_secret_access_key="your-secret-key"
)
```

## Image Processing

### DALL-E Integration

```python
from paniki.services.openai import OpenAIImageService

image_service = OpenAIImageService(
    api_key="your-api-key"
)
```

## Video Processing

### Simli Integration

```python
from paniki.services.simli import SimliVideoService

video_service = SimliVideoService(
    api_key="your-api-key"
)
```