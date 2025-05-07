# Transport Components

## Overview

Transport components handle the communication between clients and the Paniki server. Supported transports include:
- WebRTC
- WebSocket
- Local Audio
- Service-specific (Daily, LiveKit)

## WebRTC Transport

### Small WebRTC Transport

```python
from paniki.transports.network.small_webrtc import SmallWebRTCTransport
from paniki.transports.base_transport import TransportParams

transport = SmallWebRTCTransport(
    webrtc_connection=connection,
    params=TransportParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
        vad_analyzer=vad,
    ),
)
```

### Paniki WebRTC Transport

```python
from paniki.transports.network.paniki_webrtc import PanikiWebRTCTransport

transport = PanikiWebRTCTransport(
    connection_params=connection_params
)
```

## WebSocket Transport

### FastAPI WebSocket

```python
from paniki.transports.network.fastapi_websocket import FastAPIWebSocketTransport

transport = FastAPIWebSocketTransport(
    websocket=websocket
)
```

### WebSocket Server

```python
from paniki.transports.network.websocket_server import WebSocketServer

server = WebSocketServer(
    host="0.0.0.0",
    port=8080
)
```

## Local Transport

### Local Audio

```python
from paniki.transports.local.audio import LocalAudioTransport

transport = LocalAudioTransport(
    input_device=0,
    output_device=1
)
```

## Service Integration

### Daily Integration

```python
from paniki.transports.services.daily import DailyTransport

transport = DailyTransport(
    api_key="your-api-key"
)
```

### LiveKit Integration

```python
from paniki.transports.services.livekit import LiveKitTransport

transport = LiveKitTransport(
    api_key="your-api-key",
    api_secret="your-api-secret"
)
```

## Event Handling

```python
@transport.event_handler("on_client_connected")
async def on_client_connected(transport, client):
    logger.info(f"Client connected: {client}")

@transport.event_handler("on_client_disconnected")
async def on_client_disconnected(transport, client):
    logger.info(f"Client disconnected: {client}")

@transport.event_handler("on_error")
async def on_error(transport, error):
    logger.error(f"Transport error: {error}")
```

## Configuration

### Transport Parameters

```python
params = TransportParams(
    audio_in_enabled=True,
    audio_out_enabled=True,
    video_in_enabled=False,
    video_out_enabled=False,
    vad_analyzer=vad_analyzer,
    audio_out_10ms_chunks=2,
)
```

## Best Practices

1. Error Handling
```python
try:
    await transport.connect()
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
```

2. Resource Cleanup
```python
async def cleanup():
    await transport.disconnect()
    await transport.close()
```

3. Connection Management
```python
if transport.is_connected():
    await transport.send_frame(frame)
else:
    await transport.reconnect()
```