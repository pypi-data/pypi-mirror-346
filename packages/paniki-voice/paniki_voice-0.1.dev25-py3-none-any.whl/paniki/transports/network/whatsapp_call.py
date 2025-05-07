import asyncio
from dataclasses import dataclass
from typing import Dict, Optional

import aiohttp
from loguru import logger

from paniki.audio.vad.vad_analyzer import VADAnalyzer
from paniki.frames.frames import AudioRawFrame, Frame, TextFrame
from paniki.processors.frame_processor import FrameProcessor
from paniki.serializers.base_serializer import FrameSerializer
from paniki.transports.base_transport import BaseTransport


@dataclass
class WhatsappCallParams:
    """Parameters for WhatsApp call transport.

    Attributes:
        serializer: Frame serializer instance
        audio_in_enabled: Enable audio input
        audio_out_enabled: Enable audio output
        add_wav_header: Add WAV header to audio frames
        vad_analyzer: Voice activity detection analyzer
        whatsapp_phone: WhatsApp phone number
        whatsapp_token: WhatsApp API token
    """

    serializer: FrameSerializer
    audio_in_enabled: bool = True
    audio_out_enabled: bool = True
    add_wav_header: bool = True
    vad_analyzer: Optional[VADAnalyzer] = None
    whatsapp_phone: str = ""
    whatsapp_token: str = ""


class WhatsappCallClient:
    """WhatsApp call client implementation."""

    def __init__(self, phone_number: str):
        self.phone_number = phone_number
        self.remote_address = f"whatsapp:{phone_number}"
        self._is_connected = True

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    async def disconnect(self):
        self._is_connected = False


class WhatsappCallTransport(BaseTransport):
    """WhatsApp call transport implementation."""

    def __init__(self, params: WhatsappCallParams):
        super().__init__()
        self.params = params
        self._clients: Dict[str, WhatsappCallClient] = {}
        self._audio_queues = {}
        self._session = None

        # Register event handlers
        self._register_event_handler("on_client_connected")
        self._register_event_handler("on_client_disconnected")
        self._register_event_handler("on_session_timeout")

        # WhatsApp API endpoints
        self.api_version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"

    async def send_frame(self, client: WhatsappCallClient, frame: Frame):
        """Send a frame to the WhatsApp call client."""
        if isinstance(frame, AudioRawFrame) and self.params.audio_out_enabled:
            # Send audio data to WhatsApp
            try:
                # Convert audio data to appropriate format if needed
                # Send to WhatsApp API
                logger.debug(f"Sending audio frame to {client.remote_address}")
            except Exception as e:
                logger.error(f"Error sending audio frame to {client.remote_address}: {e}")
        elif isinstance(frame, TextFrame):
            try:
                # Send text message using WhatsApp API
                async with aiohttp.ClientSession() as session:
                    url = f"{self.base_url}/{self.params.whatsapp_phone}/messages"
                    headers = {
                        "Authorization": f"Bearer {self.params.whatsapp_token}",
                        "Content-Type": "application/json"
                    }
                    data = {
                        "messaging_product": "whatsapp",
                        "to": client.phone_number,
                        "type": "text",
                        "text": {"body": frame.text}
                    }
                    async with session.post(url, headers=headers, json=data) as response:
                        if response.status != 200:
                            logger.error(f"Error sending text message: {await response.text()}")
                        else:
                            logger.debug(f"Sent text message to {client.remote_address}")
            except Exception as e:
                logger.error(f"Error sending text message to {client.remote_address}: {e}")

    async def handle_incoming_audio(self, phone_number: str, audio_data: bytes):
        """Handle incoming audio data from WhatsApp call."""
        if not self.params.audio_in_enabled:
            return

        # Create or get client
        client = self._get_or_create_client(phone_number)

        # Create audio frame
        frame = AudioRawFrame(
            data=audio_data,
            add_wav_header=self.params.add_wav_header,
        )

        # Apply VAD if enabled
        if self.params.vad_analyzer:
            frame.is_speech = self.params.vad_analyzer.is_speech(audio_data)

        # Queue frame for processing
        if client.remote_address not in self._audio_queues:
            self._audio_queues[client.remote_address] = asyncio.Queue()
        await self._audio_queues[client.remote_address].put(frame)

    def _get_or_create_client(self, phone_number: str) -> WhatsappCallClient:
        """Get existing client or create new one."""
        remote_address = f"whatsapp:{phone_number}"
        if remote_address not in self._clients:
            client = WhatsappCallClient(phone_number)
            self._clients[remote_address] = client
            asyncio.create_task(self.emit("on_client_connected", client))
        return self._clients[remote_address]

    async def _cleanup_client(self, client: WhatsappCallClient):
        """Clean up client resources."""
        if client.remote_address in self._clients:
            del self._clients[client.remote_address]
        if client.remote_address in self._audio_queues:
            del self._audio_queues[client.remote_address]
        await self.emit("on_client_disconnected", client)

    def input(self) -> FrameProcessor:
        """Get input transport."""
        return self

    def output(self) -> FrameProcessor:
        """Get output transport."""
        return self

    async def process_frame(self, frame: Frame) -> Frame:
        """Process incoming frame."""
        return frame

    async def queue_frame(self, frame: Frame, direction: int):
        """Queue a frame for processing."""
        await self.process_frame(frame)

    def set_parent(self, parent):
        """Set parent pipeline."""
        self._parent = parent

    def link(self, next_processor: FrameProcessor):
        """Link this processor to the next one."""
        self._next = next_processor

    async def start(self):
        """Start the WhatsApp call transport."""
        logger.info("Starting WhatsApp call transport")
        self._session = aiohttp.ClientSession()

    async def stop(self):
        """Stop the WhatsApp call transport."""
        logger.info("Stopping WhatsApp call transport")
        
        # Disconnect all clients
        for client in list(self._clients.values()):
            await client.disconnect()
        
        # Close aiohttp session
        if self._session:
            await self._session.close()
            self._session = None

