# Frames API Reference

## Overview

Frames are the fundamental data units in Paniki that flow through the pipeline. They represent different types of data such as audio, video, text, or any custom data type.

## Base Frame

```python
from paniki.frames import Frame
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class Frame:
    """Base class for all frame types."""
    timestamp: float
    metadata: Optional[dict] = None
```

## Audio Frame

```python
@dataclass
class AudioFrame(Frame):
    """Represents audio data in the pipeline."""
    data: bytes
    sample_rate: int = 16000
    num_channels: int = 1
    sample_width: int = 2  # bytes per sample
    
    @property
    def duration(self) -> float:
        """Duration of audio in seconds."""
        return len(self.data) / (self.sample_rate * self.num_channels * self.sample_width)
```

## Text Frame

```python
@dataclass
class TextFrame(Frame):
    """Represents text data in the pipeline."""
    text: str
    language: Optional[str] = None
    confidence: Optional[float] = None
```

## Video Frame

```python
@dataclass
class VideoFrame(Frame):
    """Represents video data in the pipeline."""
    data: bytes
    width: int
    height: int
    format: str = "rgb24"
    fps: Optional[float] = None
```

## Image Frame

```python
@dataclass
class ImageFrame(Frame):
    """Represents image data in the pipeline."""
    data: bytes
    width: int
    height: int
    format: str = "rgb24"
```

## Function Frame

```python
@dataclass
class FunctionFrame(Frame):
    """Represents function calls in the pipeline."""
    name: str
    arguments: dict
    result: Optional[Any] = None
```

## Context Frame

```python
@dataclass
class ContextFrame(Frame):
    """Represents conversation context in the pipeline."""
    messages: list[dict]
    system_instruction: Optional[str] = None
```

## Custom Frame Types

### Creating Custom Frames

```python
@dataclass
class CustomFrame(Frame):
    """Custom frame type for specific use cases."""
    data: Any
    content_type: str
    
    def validate(self) -> bool:
        """Validate frame data."""
        if not self.data:
            raise ValueError("Frame data cannot be empty")
        return True
```

## Frame Utilities

### Frame Conversion

```python
from paniki.frames import convert_frame

def convert_to_audio_frame(frame: Frame) -> AudioFrame:
    """Convert a frame to AudioFrame."""
    if isinstance(frame, AudioFrame):
        return frame
    # Implement conversion logic
    raise TypeError(f"Cannot convert {type(frame)} to AudioFrame")
```

### Frame Serialization

```python
from paniki.frames import serialize_frame, deserialize_frame

def serialize_to_protobuf(frame: Frame) -> bytes:
    """Serialize frame to protobuf format."""
    return serialize_frame(frame)

def deserialize_from_protobuf(data: bytes) -> Frame:
    """Deserialize frame from protobuf format."""
    return deserialize_frame(data)
```

## Frame Processing

### Frame Filtering

```python
from paniki.processors.filters import FrameFilter

class AudioFrameFilter(FrameFilter):
    """Filter to process only AudioFrames."""
    async def filter_frame(self, frame: Frame) -> bool:
        return isinstance(frame, AudioFrame)
```

### Frame Transformation

```python
from paniki.processors.frame_processor import FrameProcessor

class FrameTransformer(FrameProcessor):
    """Transform frames from one type to another."""
    async def process_frame(self, frame: Frame) -> Frame:
        if isinstance(frame, AudioFrame):
            return self.transform_audio(frame)
        elif isinstance(frame, TextFrame):
            return self.transform_text(frame)
        return frame
```

## Best Practices

### Frame Handling

1. Always validate frame data:
```python
def process_audio_frame(frame: AudioFrame):
    if not frame.data or len(frame.data) == 0:
        raise ValueError("Empty audio frame")
    if frame.sample_rate <= 0:
        raise ValueError("Invalid sample rate")
```

2. Use type hints and validation:
```python
from typing import TypeVar, Generic

T = TypeVar('T', bound=Frame)

class FrameProcessor(Generic[T]):
    def process(self, frame: T) -> T:
        self.validate(frame)
        return self.process_frame(frame)
```

3. Handle frame metadata:
```python
def process_frame_with_metadata(frame: Frame):
    if frame.metadata:
        # Process metadata
        pass
    # Process frame data
```

### Memory Management

1. Efficient frame creation:
```python
def create_audio_frame(data: bytes, **kwargs) -> AudioFrame:
    return AudioFrame(
        data=data,
        timestamp=time.time(),
        metadata=kwargs.get('metadata'),
        sample_rate=kwargs.get('sample_rate', 16000)
    )
```

2. Frame cleanup:
```python
def cleanup_frame(frame: Frame):
    """Release any resources held by the frame."""
    if hasattr(frame, 'cleanup'):
        frame.cleanup()
```

## Error Handling

### Frame Validation Errors

```python
class FrameValidationError(Exception):
    """Raised when frame validation fails."""
    pass

def validate_frame(frame: Frame):
    try:
        if hasattr(frame, 'validate'):
            frame.validate()
    except Exception as e:
        raise FrameValidationError(f"Frame validation failed: {e}")
```

### Frame Processing Errors

```python
class FrameProcessingError(Exception):
    """Raised when frame processing fails."""
    pass

async def safe_process_frame(processor: FrameProcessor, frame: Frame) -> Frame:
    try:
        return await processor.process_frame(frame)
    except Exception as e:
        raise FrameProcessingError(f"Frame processing failed: {e}")
```