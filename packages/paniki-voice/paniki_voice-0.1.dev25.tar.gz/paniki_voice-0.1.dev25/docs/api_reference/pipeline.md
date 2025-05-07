# Pipeline API Reference

## Overview

The Pipeline system is the core of Paniki's architecture, providing a flexible way to process frames through a series of components.

## Base Pipeline

```python
from paniki.pipeline.base_pipeline import BasePipeline
from typing import List, Optional

class BasePipeline:
    """Base class for all pipeline types."""
    
    def __init__(self, components: List[Any]):
        self.components = components
        self.observers = []
    
    async def process_frame(self, frame: Frame) -> Optional[Frame]:
        """Process a frame through the pipeline."""
        raise NotImplementedError
```

## Sequential Pipeline

```python
from paniki.pipeline.pipeline import Pipeline

class Pipeline(BasePipeline):
    """Sequential pipeline implementation."""
    
    async def process_frame(self, frame: Frame) -> Optional[Frame]:
        current_frame = frame
        for component in self.components:
            if current_frame is None:
                break
            current_frame = await component.process_frame(current_frame)
        return current_frame
```

## Parallel Pipeline

```python
from paniki.pipeline.parallel_pipeline import ParallelPipeline
import asyncio

class ParallelPipeline(BasePipeline):
    """Parallel pipeline implementation."""
    
    async def process_frame(self, frame: Frame) -> List[Optional[Frame]]:
        tasks = [
            component.process_frame(frame)
            for component in self.components
        ]
        return await asyncio.gather(*tasks)
```

## Pipeline Task

```python
from paniki.pipeline.task import PipelineTask, PipelineParams
from typing import Optional

class PipelineParams:
    """Parameters for pipeline task execution."""
    def __init__(
        self,
        allow_interruptions: bool = False,
        max_idle_time: Optional[float] = None,
        max_response_time: Optional[float] = None
    ):
        self.allow_interruptions = allow_interruptions
        self.max_idle_time = max_idle_time
        self.max_response_time = max_response_time

class PipelineTask:
    """Manages pipeline execution."""
    
    def __init__(
        self,
        pipeline: BasePipeline,
        params: Optional[PipelineParams] = None
    ):
        self.pipeline = pipeline
        self.params = params or PipelineParams()
        
    async def run(self):
        """Run the pipeline task."""
        while not self.should_stop:
            frame = await self.get_next_frame()
            if frame:
                await self.pipeline.process_frame(frame)
```

## Pipeline Runner

```python
from paniki.pipeline.runner import PipelineRunner

class PipelineRunner:
    """Manages multiple pipeline tasks."""
    
    def __init__(self, handle_sigint: bool = True):
        self.tasks = []
        self.handle_sigint = handle_sigint
        
    async def run(self, task: PipelineTask):
        """Run a pipeline task."""
        self.tasks.append(task)
        try:
            await task.run()
        finally:
            await self.cleanup()
```

## Pipeline Components

### Frame Processor

```python
from paniki.processors.frame_processor import FrameProcessor

class FrameProcessor:
    """Base class for frame processors."""
    
    async def process_frame(self, frame: Frame) -> Optional[Frame]:
        """Process a single frame."""
        raise NotImplementedError
```

### Consumer Processor

```python
from paniki.processors.consumer_processor import ConsumerProcessor

class ConsumerProcessor(FrameProcessor):
    """Processor that consumes frames without producing output."""
    
    async def process_frame(self, frame: Frame) -> None:
        """Process and consume a frame."""
        await self.consume_frame(frame)
        return None
```

### Producer Processor

```python
from paniki.processors.producer_processor import ProducerProcessor

class ProducerProcessor(FrameProcessor):
    """Processor that produces frames."""
    
    async def process_frame(self, frame: Frame) -> Frame:
        """Process and produce a new frame."""
        return await self.produce_frame()
```

## Pipeline Observers

```python
from paniki.pipeline.task_observer import TaskObserver

class TaskObserver:
    """Observer for pipeline task events."""
    
    async def on_task_started(self, task: PipelineTask):
        """Called when task starts."""
        pass
        
    async def on_task_completed(self, task: PipelineTask):
        """Called when task completes."""
        pass
        
    async def on_task_error(self, task: PipelineTask, error: Exception):
        """Called when task encounters an error."""
        pass
```

## Pipeline Metrics

```python
from paniki.metrics import PipelineMetrics

class PipelineMetrics(TaskObserver):
    """Collects pipeline performance metrics."""
    
    def __init__(self):
        self.processed_frames = 0
        self.errors = 0
        self.processing_times = []
        
    async def on_frame_processed(self, frame: Frame, duration: float):
        """Record frame processing metrics."""
        self.processed_frames += 1
        self.processing_times.append(duration)
```

## Best Practices

### Error Handling

```python
class ResilientPipeline(Pipeline):
    """Pipeline with error handling."""
    
    async def process_frame(self, frame: Frame) -> Optional[Frame]:
        try:
            return await super().process_frame(frame)
        except Exception as e:
            await self.handle_error(e)
            return None
            
    async def handle_error(self, error: Exception):
        """Handle pipeline errors."""
        for observer in self.observers:
            await observer.on_error(error)
```

### Resource Management

```python
class ManagedPipeline(Pipeline):
    """Pipeline with resource management."""
    
    async def __aenter__(self):
        """Setup pipeline resources."""
        await self.setup()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup pipeline resources."""
        await self.cleanup()
        
    async def setup(self):
        """Setup pipeline components."""
        for component in self.components:
            if hasattr(component, 'setup'):
                await component.setup()
                
    async def cleanup(self):
        """Cleanup pipeline components."""
        for component in self.components:
            if hasattr(component, 'cleanup'):
                await component.cleanup()
```

### Performance Optimization

```python
class OptimizedPipeline(Pipeline):
    """Pipeline with performance optimizations."""
    
    def __init__(self, components: List[Any], buffer_size: int = 100):
        super().__init__(components)
        self.frame_buffer = asyncio.Queue(maxsize=buffer_size)
        
    async def process_frame(self, frame: Frame) -> Optional[Frame]:
        """Process frame with buffering."""
        await self.frame_buffer.put(frame)
        return await self.process_buffered_frames()
```