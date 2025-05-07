# Configuration Guide

## Environment Variables

Create a `.env` file in your project root:

```bash
# AI Service API Keys
OPENAI_API_KEY=your-openai-key
GOOGLE_API_KEY=your-google-key
ANTHROPIC_API_KEY=your-anthropic-key
ELEVENLABS_API_KEY=your-elevenlabs-key

# AWS Credentials
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1

# Azure Credentials
AZURE_API_KEY=your-azure-key
AZURE_REGION=eastus

# Service Configuration
PANIKI_LOG_LEVEL=INFO
PANIKI_HOST=0.0.0.0
PANIKI_PORT=8080
```

## Service Configuration

### LLM Configuration

```python
from paniki.services.openai import OpenAILLMService
from paniki.transcriptions.language import Language

llm = OpenAILLMService(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4-turbo-preview",
    temperature=0.7,
    max_tokens=150,
    system_instruction="""
    You are a helpful assistant...
    """,
    language=Language.EN_US
)
```

### Speech-to-Text Configuration

```python
from paniki.services.whisper import WhisperSTTService

stt = WhisperSTTService(
    model="large-v3",
    language="en",
    task="transcribe",
    compute_type="float16"
)
```

### Text-to-Speech Configuration

```python
from paniki.services.elevenlabs import ElevenLabsTTSService

tts = ElevenLabsTTSService(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
    voice_id="voice-id",
    model="eleven_multilingual_v2",
    optimize_streaming_latency=2
)
```

## Transport Configuration

### WebRTC Configuration

```python
from paniki.transports.network.small_webrtc import SmallWebRTCTransport
from paniki.audio.vad.silero import SileroVADAnalyzer

transport = SmallWebRTCTransport(
    webrtc_connection=connection,
    params=TransportParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
        video_in_enabled=False,
        video_out_enabled=False,
        vad_analyzer=SileroVADAnalyzer(),
        audio_out_10ms_chunks=2,
    ),
)
```

### WebSocket Configuration

```python
from paniki.transports.network.websocket_server import WebSocketServer

server = WebSocketServer(
    host=os.getenv("PANIKI_HOST", "0.0.0.0"),
    port=int(os.getenv("PANIKI_PORT", 8080)),
    ssl_context=None  # Configure SSL if needed
)
```

## Pipeline Configuration

```python
from paniki.pipeline.pipeline import Pipeline
from paniki.pipeline.task import PipelineTask, PipelineParams

pipeline = Pipeline([
    transport.input(),
    stt_service,
    llm_service,
    tts_service,
    transport.output(),
])

task = PipelineTask(
    pipeline,
    params=PipelineParams(
        allow_interruptions=False,
        max_idle_time=30.0,
        max_response_time=10.0
    ),
)
```

## Logging Configuration

```python
from loguru import logger

logger.add(
    "paniki.log",
    rotation="1 day",
    retention="7 days",
    level=os.getenv("PANIKI_LOG_LEVEL", "INFO")
)
```

## Metrics Configuration

```python
from paniki.metrics import PipelineMetrics
from paniki.services.canonical import CanonicalMetricsService

metrics = PipelineMetrics()
metrics_service = CanonicalMetricsService(
    endpoint="your-metrics-endpoint"
)

pipeline.add_observer(metrics)
metrics.add_observer(metrics_service)
```

## Security Configuration

```python
# SSL/TLS Configuration
ssl_context = ssl.create_default_context(
    purpose=ssl.Purpose.CLIENT_AUTH
)
ssl_context.load_cert_chain(
    certfile="path/to/cert.pem",
    keyfile="path/to/key.pem"
)

# API Key Authentication
def validate_api_key(api_key: str) -> bool:
    return api_key == os.getenv("PANIKI_API_KEY")
```