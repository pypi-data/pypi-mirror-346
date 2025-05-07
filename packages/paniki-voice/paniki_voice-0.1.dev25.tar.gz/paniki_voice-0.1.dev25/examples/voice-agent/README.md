# Voice Agent

A WhatsApp voice bot that uses Gemini for conversation and text-to-speech.

## Features

- WhatsApp voice call integration
- Speech-to-text using Deepgram
- Natural language processing using Gemini
- Text-to-speech using Google Cloud TTS
- Voice activity detection using Silero VAD

## Prerequisites

- Docker and Docker Compose
- Google Cloud API key
- Deepgram API key
- OpenAI API key
- WhatsApp Business API credentials

## Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your API keys
3. Build and run with Docker Compose:

```bash
docker-compose up --build
```

The server will be available at http://localhost:8080.

## Environment Variables

- `GOOGLE_API_KEY`: Google API key for Gemini
- `DEEPGRAM_API_KEY`: Deepgram API key for speech-to-text
- `OPENAI_API_KEY`: OpenAI API key for LLM
- `FBTOKEN`: WhatsApp Business API token
- `PHONEID`: WhatsApp Business API phone ID

## Architecture

The voice agent uses a pipeline architecture:

1. WhatsApp voice call -> WebRTC audio stream
2. Audio stream -> Speech-to-text (Deepgram)
3. Text -> Natural language processing (Gemini)
4. Response -> Text-to-speech (Google Cloud TTS)
5. Audio response -> WhatsApp voice call

Voice activity detection (Silero VAD) is used to detect when the user starts and stops speaking.

---

## WebRTC ICE Servers Configuration

When implementing WebRTC in your project, **STUN** (Session Traversal Utilities for NAT) and **TURN** (Traversal Using Relays around NAT) 
servers are usually needed in cases where users are behind routers or firewalls.

In local networks (e.g., testing within the same home or office network), you usually don’t need to configure STUN or TURN servers. 
In such cases, WebRTC can often directly establish peer-to-peer connections without needing to traverse NAT or firewalls.

### What are STUN and TURN Servers?

- **STUN Server**: Helps clients discover their public IP address and port when they're behind a NAT (Network Address Translation) device (like a router). 
This allows WebRTC to attempt direct peer-to-peer communication by providing the public-facing IP and port.
  
- **TURN Server**: Used as a fallback when direct peer-to-peer communication isn't possible due to strict NATs or firewalls blocking connections. 
The TURN server relays media traffic between peers.

### Why are ICE Servers Important?

**ICE (Interactive Connectivity Establishment)** is a framework used by WebRTC to handle network traversal and NAT issues. 
The `iceServers` configuration provides a list of **STUN** and **TURN** servers that WebRTC uses to find the best way to connect two peers. 

### Example Configuration for ICE Servers

Here’s how you can configure a basic `iceServers` object in WebRTC for testing purposes, using Google's public STUN server:

```javascript
const config = {
  iceServers: [
    {
      urls: ["stun:stun.l.google.com:19302"], // Google's public STUN server
    }
  ],
};
```

> For testing purposes, you can either use public **STUN** servers (like Google's) or set up your own **TURN** server. 
If you're running your own TURN server, make sure to include your server URL, username, and credential in the configuration.

---

### 💡 Notes
- Ensure all dependencies are installed before running the server.
- Check the `.env` file for missing configurations.
- WebRTC requires a secure environment (HTTPS) for full functionality in production.

Happy coding! 🎉