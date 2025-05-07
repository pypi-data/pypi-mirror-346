# Advanced Usage Guide

## Custom Components

### Creating Custom Processors

```python
from paniki.processors.frame_processor import FrameProcessor
from paniki.frames import AudioFrame, TextFrame

class CustomAudioProcessor(FrameProcessor):
    def __init__(self, config):
        super().__init__()
        self.config = config

    async def process_frame(self, frame):
        if isinstance(frame, AudioFrame):
            # Process audio data
            processed_data = self.process_audio(frame.data)
            return AudioFrame(data=processed_data)
        return frame

    def process_audio(self, data):
        # Custom audio processing logic
        return processed_data
```

### Custom AI Service Integration

```python
from paniki.services.llm_service import LLMService
from paniki.adapters.base_llm_adapter import BaseLLMAdapter

class CustomLLMService(LLMService):
    def __init__(self, api_key, **kwargs):
        super().__init__()
        self.api_key = api_key
        self.adapter = CustomLLMAdapter()

    async def process_frame(self, frame):
        if isinstance(frame, TextFrame):
            response = await self.adapter.generate_response(
                frame.text,
                self.api_key
            )
            return TextFrame(text=response)
        return frame
```

## Advanced Pipeline Patterns

### Multi-Modal Processing

```python
from paniki.pipeline.parallel_pipeline import ParallelPipeline

# Audio pipeline
audio_pipeline = Pipeline([
    audio_input,
    audio_processor,
    stt_service,
])

# Video pipeline
video_pipeline = Pipeline([
    video_input,
    video_processor,
    vision_service,
])

# Text pipeline
text_pipeline = Pipeline([
    llm_service,
    tts_service,
])

# Combine pipelines
multi_modal_pipeline = ParallelPipeline([
    audio_pipeline,
    video_pipeline,
    text_pipeline,
])
```

### Pipeline Branching

```python
from paniki.pipeline.pipeline import Pipeline
from paniki.processors.filters import FrameFilter

class ContentTypeFilter(FrameFilter):
    def __init__(self, content_type):
        self.content_type = content_type

    async def filter_frame(self, frame):
        return frame.content_type == self.content_type

# Create branched pipeline
pipeline = Pipeline([
    input_processor,
    [
        (ContentTypeFilter("audio"), audio_pipeline),
        (ContentTypeFilter("video"), video_pipeline),
        (ContentTypeFilter("text"), text_pipeline),
    ],
    output_processor,
])
```

## Advanced Audio Processing

### Custom VAD Implementation

```python
from paniki.audio.vad.vad_analyzer import VADAnalyzer
import numpy as np

class CustomVAD(VADAnalyzer):
    def __init__(self, threshold=0.5):
        self.threshold = threshold

    def analyze_frame(self, frame_data):
        energy = np.mean(np.abs(frame_data))
        return energy > self.threshold

    def get_speech_probability(self, frame_data):
        energy = np.mean(np.abs(frame_data))
        return min(energy / self.threshold, 1.0)
```

### Advanced Audio Filtering

```python
from paniki.audio.filters.base_audio_filter import BaseAudioFilter
import numpy as np
from scipy import signal

class AdvancedAudioFilter(BaseAudioFilter):
    def __init__(self, filter_type="bandpass", cutoff=(300, 3400)):
        self.filter_type = filter_type
        self.cutoff = cutoff
        self.sample_rate = 16000

    def process_frame(self, frame_data):
        nyquist = self.sample_rate / 2
        b, a = signal.butter(
            4,
            [f/nyquist for f in self.cutoff],
            self.filter_type
        )
        return signal.filtfilt(b, a, frame_data)
```

## Advanced AI Integration

### Multi-Model Orchestration

```python
from paniki.services.ai_services import AIService
from paniki.processors.aggregators import LLMResponse

class MultiModelOrchestrator(AIService):
    def __init__(self, models, weights=None):
        self.models = models
        self.weights = weights or [1/len(models)] * len(models)

    async def process_frame(self, frame):
        responses = []
        for model in self.models:
            response = await model.process_frame(frame)
            responses.append(response)

        return self.aggregate_responses(responses)

    def aggregate_responses(self, responses):
        # Implement custom response aggregation logic
        pass
```

### Context Management

```python
from paniki.processors.aggregators import OpenAILLMContext

class AdvancedContext(OpenAILLMContext):
    def __init__(self, max_tokens=4000):
        super().__init__()
        self.max_tokens = max_tokens
        self.token_count = 0

    def add_message(self, role, content):
        # Add token counting logic
        self.token_count += self.count_tokens(content)
        if self.token_count > self.max_tokens:
            self.trim_context()
        super().add_message(role, content)

    def trim_context(self):
        # Implement context trimming logic
        pass
```

## Performance Optimization

### Memory Management

```python
class MemoryOptimizedPipeline(Pipeline):
    def __init__(self, components, buffer_size=1000):
        super().__init__(components)
        self.buffer_size = buffer_size
        self.frame_buffer = []

    async def process_frame(self, frame):
        result = await super().process_frame(frame)
        self.frame_buffer.append(result)
        
        if len(self.frame_buffer) > self.buffer_size:
            self.frame_buffer = self.frame_buffer[-self.buffer_size:]
        
        return result
```

### Parallel Processing

```python
from concurrent.futures import ThreadPoolExecutor
import asyncio

class ParallelProcessor(FrameProcessor):
    def __init__(self, max_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    async def process_frame(self, frame):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self.process_in_thread,
            frame
        )

    def process_in_thread(self, frame):
        # Implement CPU-intensive processing here
        pass
```

## Testing and Validation

### Frame Validation

```python
from paniki.frames import Frame
from dataclasses import dataclass
from typing import Optional

@dataclass
class ValidatedFrame(Frame):
    data: bytes
    timestamp: float
    sequence_number: int
    checksum: Optional[str] = None

    def validate(self):
        if not self.data:
            raise ValueError("Frame data cannot be empty")
        if self.timestamp < 0:
            raise ValueError("Invalid timestamp")
        if self.sequence_number < 0:
            raise ValueError("Invalid sequence number")
        return True
```

### Pipeline Testing

```python
import pytest
from paniki.pipeline.pipeline import Pipeline

@pytest.fixture
async def test_pipeline():
    components = [
        TestInputProcessor(),
        TestProcessor(),
        TestOutputProcessor(),
    ]
    pipeline = Pipeline(components)
    yield pipeline
    await pipeline.cleanup()

async def test_pipeline_processing(test_pipeline):
    input_frame = TestFrame(data="test")
    result = await test_pipeline.process_frame(input_frame)
    assert result.data == "processed"
```