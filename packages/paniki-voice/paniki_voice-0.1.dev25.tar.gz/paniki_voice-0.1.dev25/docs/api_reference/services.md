# Services API Reference

## Overview

Paniki services provide integration with various AI and media processing services, including:
- Language Models (LLM)
- Speech-to-Text (STT)
- Text-to-Speech (TTS)
- Image Processing
- Video Processing

## Base Service Classes

### AI Service

```python
from paniki.services.ai_service import AIService
from typing import Optional

class AIService:
    """Base class for AI services."""
    
    async def process_frame(self, frame: Frame) -> Optional[Frame]:
        """Process a frame using the AI service."""
        raise NotImplementedError
```

### LLM Service

```python
from paniki.services.llm_service import LLMService
from typing import List, Dict

class LLMService(AIService):
    """Base class for Language Model services."""
    
    def __init__(
        self,
        system_instruction: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ):
        self.system_instruction = system_instruction
        self.temperature = temperature
        self.max_tokens = max_tokens
        
    async def generate_response(
        self,
        messages: List[Dict[str, str]]
    ) -> str:
        """Generate response from messages."""
        raise NotImplementedError
```

### STT Service

```python
from paniki.services.stt_service import STTService
from paniki.transcriptions.language import Language

class STTService(AIService):
    """Base class for Speech-to-Text services."""
    
    def __init__(
        self,
        language: Language = Language.EN_US,
        model: Optional[str] = None
    ):
        self.language = language
        self.model = model
        
    async def transcribe_audio(
        self,
        audio_data: bytes,
        sample_rate: int = 16000
    ) -> str:
        """Transcribe audio data to text."""
        raise NotImplementedError
```

### TTS Service

```python
from paniki.services.tts_service import TTSService

class TTSService(AIService):
    """Base class for Text-to-Speech services."""
    
    def __init__(
        self,
        voice_id: Optional[str] = None,
        language: Language = Language.EN_US
    ):
        self.voice_id = voice_id
        self.language = language
        
    async def synthesize_speech(
        self,
        text: str
    ) -> bytes:
        """Synthesize text to speech."""
        raise NotImplementedError
```

## Service Implementations

### OpenAI Service

```python
from paniki.services.openai import OpenAILLMService

class OpenAILLMService(LLMService):
    """OpenAI GPT service implementation."""
    
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4-turbo-preview",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.api_key = api_key
        self.model = model
        
    async def generate_response(
        self,
        messages: List[Dict[str, str]]
    ) -> str:
        """Generate response using OpenAI API."""
        # Implementation details
```

### Whisper Service

```python
from paniki.services.whisper import WhisperSTTService

class WhisperSTTService(STTService):
    """Whisper speech recognition service."""
    
    def __init__(
        self,
        model: str = "large-v3",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.model = model
        
    async def transcribe_audio(
        self,
        audio_data: bytes,
        sample_rate: int = 16000
    ) -> str:
        """Transcribe audio using Whisper."""
        # Implementation details
```

### ElevenLabs Service

```python
from paniki.services.elevenlabs import ElevenLabsTTSService

class ElevenLabsTTSService(TTSService):
    """ElevenLabs text-to-speech service."""
    
    def __init__(
        self,
        api_key: str,
        voice_id: str,
        **kwargs
    ):
        super().__init__(voice_id=voice_id, **kwargs)
        self.api_key = api_key
        
    async def synthesize_speech(
        self,
        text: str
    ) -> bytes:
        """Synthesize speech using ElevenLabs."""
        # Implementation details
```

## Service Adapters

### Base Adapter

```python
from paniki.adapters.base_llm_adapter import BaseLLMAdapter

class BaseLLMAdapter:
    """Base class for LLM service adapters."""
    
    async def generate_response(
        self,
        prompt: str,
        **kwargs
    ) -> str:
        """Generate response using the service."""
        raise NotImplementedError
```

### OpenAI Adapter

```python
from paniki.adapters.services.open_ai_adapter import OpenAIAdapter

class OpenAIAdapter(BaseLLMAdapter):
    """Adapter for OpenAI API."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        
    async def generate_response(
        self,
        prompt: str,
        **kwargs
    ) -> str:
        """Generate response using OpenAI."""
        # Implementation details
```

## Service Configuration

### API Configuration

```python
class APIConfig:
    """Configuration for API services."""
    
    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
        max_retries: int = 3
    ):
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
```

### Service Factory

```python
class ServiceFactory:
    """Factory for creating service instances."""
    
    @staticmethod
    def create_llm_service(
        provider: str,
        api_key: str,
        **kwargs
    ) -> LLMService:
        """Create LLM service instance."""
        if provider == "openai":
            return OpenAILLMService(api_key, **kwargs)
        elif provider == "anthropic":
            return AnthropicLLMService(api_key, **kwargs)
        raise ValueError(f"Unknown provider: {provider}")
```

## Best Practices

### Error Handling

```python
class ServiceError(Exception):
    """Base class for service errors."""
    pass

class APIError(ServiceError):
    """API-related errors."""
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code

async def handle_api_error(func):
    """Decorator for handling API errors."""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            raise APIError(str(e), getattr(e, 'status_code', 500))
    return wrapper
```

### Rate Limiting

```python
from paniki.utils.network import RateLimiter

class RateLimitedService(AIService):
    """Service with rate limiting."""
    
    def __init__(self, requests_per_minute: int = 60):
        self.rate_limiter = RateLimiter(
            max_requests=requests_per_minute,
            time_window=60
        )
        
    async def process_frame(self, frame: Frame) -> Optional[Frame]:
        async with self.rate_limiter:
            return await super().process_frame(frame)
```

### Caching

```python
from functools import lru_cache
from typing import Any

class CachedService(AIService):
    """Service with response caching."""
    
    def __init__(self, cache_size: int = 1000):
        self.cache = lru_cache(maxsize=cache_size)(self._generate_response)
        
    async def _generate_response(
        self,
        prompt: str,
        **kwargs
    ) -> Any:
        """Generate and cache response."""
        # Implementation details
```