# Pipeline System

## Overview

The pipeline system is the core of Paniki's architecture, allowing for modular and flexible processing of audio, video, and text data.

## Basic Pipeline

```python
from paniki.pipeline.pipeline import Pipeline
from paniki.pipeline.task import PipelineTask, PipelineParams

# Create pipeline components
input_component = transport.input()
processing_component = llm_service
output_component = transport.output()

# Create pipeline
pipeline = Pipeline([
    input_component,
    processing_component,
    output_component,
])

# Create pipeline task
task = PipelineTask(
    pipeline,
    params=PipelineParams(
        allow_interruptions=False,
    ),
)
```

## Parallel Pipeline

```python
from paniki.pipeline.parallel_pipeline import ParallelPipeline

pipeline = ParallelPipeline([
    audio_pipeline,
    video_pipeline,
])
```

## Pipeline Components

### Frame Processors

```python
from paniki.processors.frame_processor import FrameProcessor

class CustomProcessor(FrameProcessor):
    async def process_frame(self, frame):
        # Process frame here
        return processed_frame
```

### Filters

```python
from paniki.processors.filters import FrameFilter

class CustomFilter(FrameFilter):
    async def filter_frame(self, frame):
        # Filter frame here
        return should_process
```

### Aggregators

```python
from paniki.processors.aggregators import LLMResponse

aggregator = LLMResponse()
```

## Pipeline Events

```python
@transport.event_handler("on_client_connected")
async def on_client_connected(transport, client):
    # Handle client connection
    pass

@transport.event_handler("on_client_disconnected")
async def on_client_disconnected(transport, client):
    # Handle client disconnection
    pass
```

## Pipeline Runner

```python
from paniki.pipeline.runner import PipelineRunner

runner = PipelineRunner(handle_sigint=True)
await runner.run(task)
```

## Best Practices

1. Error Handling
```python
try:
    await pipeline.process_frame(frame)
except Exception as e:
    logger.error(f"Error processing frame: {e}")
```

2. Resource Management
```python
async def cleanup():
    await task.cancel()
    await transport.close()
```

3. Monitoring
```python
from paniki.metrics import PipelineMetrics

metrics = PipelineMetrics()
pipeline.add_observer(metrics)
```