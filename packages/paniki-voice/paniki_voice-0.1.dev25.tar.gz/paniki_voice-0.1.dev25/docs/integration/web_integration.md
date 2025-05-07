# Web Integration Guide

## Overview

This guide covers integrating Paniki with web applications using WebRTC and WebSocket connections.

## WebRTC Integration

### Server Setup

```python
from paniki.transports.network.small_webrtc import SmallWebRTCTransport
from paniki.audio.vad.silero import SileroVADAnalyzer
from aiohttp import web
import json

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    # Create WebRTC transport
    transport = SmallWebRTCTransport(
        webrtc_connection=ws,
        params=TransportParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            vad_analyzer=SileroVADAnalyzer(),
        ),
    )
    
    async for msg in ws:
        if msg.type == web.WSMsgType.TEXT:
            data = json.loads(msg.data)
            if data["type"] == "offer":
                await transport.handle_offer(data["sdp"])
            elif data["type"] == "ice_candidate":
                await transport.handle_ice_candidate(data["candidate"])

app = web.Application()
app.router.add_get("/ws", websocket_handler)
web.run_app(app, host="0.0.0.0", port=8080)
```

### Client Setup

```javascript
// WebRTC client setup
const configuration = {
  iceServers: [
    { urls: "stun:stun.l.google.com:19302" }
  ]
};

class PanikiClient {
  constructor(wsUrl) {
    this.ws = new WebSocket(wsUrl);
    this.pc = new RTCPeerConnection(configuration);
    this.setupWebRTC();
  }

  async setupWebRTC() {
    // Add audio track
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    stream.getTracks().forEach(track => this.pc.addTrack(track, stream));

    // Create and send offer
    const offer = await this.pc.createOffer();
    await this.pc.setLocalDescription(offer);
    this.ws.send(JSON.stringify({
      type: "offer",
      sdp: offer.sdp
    }));

    // Handle ICE candidates
    this.pc.onicecandidate = event => {
      if (event.candidate) {
        this.ws.send(JSON.stringify({
          type: "ice_candidate",
          candidate: event.candidate
        }));
      }
    };
  }
}
```

### HTML Integration

```html
<!DOCTYPE html>
<html>
<head>
    <title>Paniki Web Client</title>
</head>
<body>
    <div id="controls">
        <button id="startBtn">Start</button>
        <button id="stopBtn">Stop</button>
    </div>
    <div id="status"></div>

    <script>
        const client = new PanikiClient("ws://localhost:8080/ws");
        
        document.getElementById("startBtn").onclick = () => {
            client.start();
        };
        
        document.getElementById("stopBtn").onclick = () => {
            client.stop();
        };
    </script>
</body>
</html>
```

## WebSocket Integration

### Server Setup

```python
from paniki.transports.network.websocket_server import WebSocketServer
from paniki.pipeline.pipeline import Pipeline

async def create_websocket_server():
    server = WebSocketServer(
        host="0.0.0.0",
        port=8080,
        ssl_context=None  # Configure SSL if needed
    )
    
    pipeline = Pipeline([
        server.input(),
        stt_service,
        llm_service,
        tts_service,
        server.output(),
    ])
    
    return server, pipeline

# Run server
server, pipeline = await create_websocket_server()
await server.start()
```

### Client Setup

```javascript
class WebSocketClient {
  constructor(url) {
    this.ws = new WebSocket(url);
    this.setupHandlers();
  }

  setupHandlers() {
    this.ws.onmessage = async (event) => {
      const data = JSON.parse(event.data);
      await this.handleMessage(data);
    };

    this.ws.onopen = () => {
      console.log("Connected to server");
    };

    this.ws.onclose = () => {
      console.log("Disconnected from server");
    };
  }

  async handleMessage(data) {
    switch (data.type) {
      case "audio":
        await this.playAudio(data.audio);
        break;
      case "text":
        this.displayText(data.text);
        break;
    }
  }

  async sendAudio(audioData) {
    this.ws.send(JSON.stringify({
      type: "audio",
      data: audioData
    }));
  }
}
```

## React Integration

### Component Setup

```jsx
import React, { useEffect, useRef } from 'react';

const PanikiComponent = () => {
  const clientRef = useRef(null);
  const audioContextRef = useRef(null);

  useEffect(() => {
    // Initialize client
    clientRef.current = new PanikiClient("ws://localhost:8080/ws");
    audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();

    return () => {
      // Cleanup
      clientRef.current?.disconnect();
      audioContextRef.current?.close();
    };
  }, []);

  const startRecording = async () => {
    try {
      await clientRef.current.start();
    } catch (error) {
      console.error("Failed to start recording:", error);
    }
  };

  const stopRecording = () => {
    clientRef.current?.stop();
  };

  return (
    <div>
      <button onClick={startRecording}>Start</button>
      <button onClick={stopRecording}>Stop</button>
    </div>
  );
};

export default PanikiComponent;
```

## Vue.js Integration

### Component Setup

```vue
<template>
  <div>
    <button @click="startRecording">Start</button>
    <button @click="stopRecording">Stop</button>
  </div>
</template>

<script>
import { PanikiClient } from './paniki-client';

export default {
  name: 'PanikiVoice',
  data() {
    return {
      client: null,
      isRecording: false
    };
  },
  mounted() {
    this.client = new PanikiClient("ws://localhost:8080/ws");
  },
  methods: {
    async startRecording() {
      try {
        await this.client.start();
        this.isRecording = true;
      } catch (error) {
        console.error("Failed to start recording:", error);
      }
    },
    stopRecording() {
      this.client?.stop();
      this.isRecording = false;
    }
  },
  beforeDestroy() {
    this.client?.disconnect();
  }
};
</script>
```

## Advanced Integration

### Media Processing

```javascript
class MediaProcessor {
  constructor() {
    this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    this.processor = this.audioContext.createScriptProcessor(1024, 1, 1);
  }

  async setupAudioProcessing(stream) {
    const source = this.audioContext.createMediaStreamSource(stream);
    source.connect(this.processor);
    this.processor.connect(this.audioContext.destination);

    this.processor.onaudioprocess = (e) => {
      const inputData = e.inputBuffer.getChannelData(0);
      this.processAudioData(inputData);
    };
  }

  processAudioData(data) {
    // Implement audio processing logic
  }
}
```

### Error Handling

```javascript
class ErrorHandler {
  static async handleMediaError(error) {
    switch (error.name) {
      case "NotAllowedError":
        throw new Error("Microphone permission denied");
      case "NotFoundError":
        throw new Error("No microphone found");
      default:
        throw new Error(`Media error: ${error.message}`);
    }
  }

  static async handleWebSocketError(error) {
    // Handle WebSocket errors
  }

  static async handleWebRTCError(error) {
    // Handle WebRTC errors
  }
}
```

### Connection Management

```javascript
class ConnectionManager {
  constructor(config) {
    this.config = config;
    this.retryCount = 0;
    this.maxRetries = 3;
  }

  async connect() {
    try {
      await this.establishConnection();
    } catch (error) {
      if (this.retryCount < this.maxRetries) {
        this.retryCount++;
        await this.reconnect();
      } else {
        throw new Error("Failed to establish connection");
      }
    }
  }

  async reconnect() {
    // Implement reconnection logic
  }
}
```