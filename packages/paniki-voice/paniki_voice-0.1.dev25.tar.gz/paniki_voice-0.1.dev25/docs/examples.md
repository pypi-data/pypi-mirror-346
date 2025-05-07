# Examples

## Voice Agent Example

The Voice Agent example demonstrates how to create an interactive voice bot using Paniki. This example showcases:
- WebRTC integration for real-time audio
- Voice Activity Detection (VAD)
- Integration with Google's Gemini for multimodal interactions
- Pipeline-based architecture

### Basic Setup

```python
from paniki.audio.vad.silero import SileroVADAnalyzer
from paniki.pipeline.pipeline import Pipeline
from paniki.pipeline.runner import PipelineRunner
from paniki.pipeline.task import PipelineParams, PipelineTask
from paniki.transports.network.small_webrtc import SmallWebRTCTransport

# Set up WebRTC transport
transport = SmallWebRTCTransport(
    webrtc_connection=webrtc_connection,
    params=TransportParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
        vad_analyzer=SileroVADAnalyzer(),
        audio_out_10ms_chunks=2,
    ),
)
```

### Creating an AI Service

```python
from paniki.services.gemini_multimodal_live.gemini import (
    GeminiMultimodalLiveLLMService,
    InputParams,
    GeminiMultimodalModalities
)

llm = GeminiMultimodalLiveLLMService(
    api_key="your-api-key",
    voice_id="Kore",  # Available voices: Aoede, Charon, Fenrir, Kore, Puck
    transcribe_user_audio=True,
    transcribe_model_audio=True,
    system_instruction="Your system prompt here",
    params=InputParams(
        temperature=0.7,
        language=Language.EN_US,
        modalities=GeminiMultimodalModalities.AUDIO
    )
)
```

### Building a Pipeline

```python
pipeline = Pipeline([
    transport.input(),           # Audio input
    context_aggregator.user(),   # Process user input
    llm,                        # AI model processing
    transport.output(),         # Audio output
    context_aggregator.assistant(), # Process assistant response
])

task = PipelineTask(
    pipeline,
    params=PipelineParams(
        allow_interruptions=False,
    ),
)
```

## WebSocket Server Example

The WebSocket server example shows how to create a server that can handle WebSocket connections for real-time communication. This is useful for web-based applications.

### Basic Setup

```python
# Example code coming soon
```

## WhatsApp Call Example

The WhatsApp call example demonstrates how to integrate Paniki with WhatsApp's voice call functionality.

### Basic Setup

```python
# Example code coming soon
```

## Running the Examples

1. Clone the repository:
```bash
git clone https://github.com/anak10thn/paniki.git
cd paniki
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp examples/voice-agent/env.example examples/voice-agent/.env
# Edit .env with your API keys and configuration
```

4. Run the example:
```bash
cd examples/voice-agent
python server.py
```