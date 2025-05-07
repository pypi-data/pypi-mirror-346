import argparse
import asyncio
import json
import os
import ssl
import uuid
import httpx
import logging

from aiohttp import web
from av import VideoFrame

from aiortc import RTCIceServer, RTCSessionDescription
from paniki.transports.network.webrtc_connection import SmallWebRTCConnection
from bot import run_bot

from dotenv import load_dotenv
load_dotenv()

ROOT = os.path.dirname(__file__)
FBTOKEN = os.getenv("WHATSAPP_TOKEN")
PHONEID = os.getenv("WHATSAPP_PHONE")

logger = logging.getLogger("pc")
connections = set()

async def accept_call(phone_number, call_id, sdp):
    """Accept an incoming WhatsApp call."""
    url = f"https://graph.facebook.com/v18.0/{PHONEID}/calls"

    payload = {
        "to": phone_number,
        "messaging_product": "whatsapp",
        "call_id": call_id,
        "action": "accept",
        "session": {
            "sdp": sdp,
            "sdp_type": "answer"
        }
    }
    logger.info(f"Send request to {url} with payload {json.dumps(payload)}")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {FBTOKEN}",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url=url, headers=headers, json=payload)
        logger.info(f"Got response: {response.text}")
        return response

async def reject_call(phone_number, call_id, action):
    """Reject or terminate a WhatsApp call."""
    url = f"https://graph.facebook.com/v18.0/{PHONEID}/calls"

    payload = {
        "to": phone_number,
        "messaging_product": "whatsapp",
        "call_id": call_id,
        "action": action
    }
    logger.info(f"Send request to {url} with payload {json.dumps(payload)}")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {FBTOKEN}",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url=url, headers=headers, json=payload)
        logger.info(f"Got response: {response.text}")
        return response

async def offer(request):
    """Handle webhook events from WhatsApp."""
    params = await request.json()
    logger.info(f"Received webhook data: {params}")

    # Handle messages (ignore)
    if params.get("messages"):
        return web.Response(
            content_type="application/json",
            text=json.dumps({}),
        )

    # Handle calls
    if params.get("calls"):
        call = params["calls"][0]
        call_id = call["id"]
        phone_number = call["from"]
        event = call.get("event", "").lower()

        if event == "connect":
            # Get WebRTC connection info
            session = call.get("session", {})
            if not session:
                logger.error("Missing session information")
                return web.Response(
                    content_type="application/json",
                    text=json.dumps({"error": "Missing session"}),
                    status=400
                )

            # Get SDP info
            sdp = session.get("sdp")
            sdp_type = session.get("sdp_type", "offer")
            if not sdp:
                logger.error("Missing SDP information")
                return web.Response(
                    content_type="application/json",
                    text=json.dumps({"error": "Missing SDP"}),
                    status=400
                )

            # Create WebRTC connection wrapper
            ice_servers = [
                RTCIceServer(urls="stun:stun.l.google.com:19302"),
            ]
            webrtc_connection = SmallWebRTCConnection(ice_servers)

            # Add event handlers
            async def on_track_started(track):
                logger.info(f"Track {track.kind} received")
                if track.kind == "audio":
                    # Start bot with this track
                    asyncio.create_task(run_bot(webrtc_connection, track))
            webrtc_connection.add_event_handler("track-started", on_track_started)

            async def on_track_ended(track):
                logger.info(f"Track {track.kind} ended")
            webrtc_connection.add_event_handler("track-ended", on_track_ended)

            async def on_connected():
                logger.info("WebRTC connection established")
            webrtc_connection.add_event_handler("connected", on_connected)

            async def on_disconnected():
                logger.info("WebRTC connection lost")
                connections.discard(webrtc_connection)
                await reject_call(phone_number, call_id, "terminate")
            webrtc_connection.add_event_handler("disconnected", on_disconnected)

            async def on_closed():
                logger.info("WebRTC connection closed")
                connections.discard(webrtc_connection)
            webrtc_connection.add_event_handler("closed", on_closed)

            async def on_failed():
                logger.info("WebRTC connection failed")
                connections.discard(webrtc_connection)
                await reject_call(phone_number, call_id, "terminate")
            webrtc_connection.add_event_handler("failed", on_failed)

            # Initialize connection
            await webrtc_connection.initialize(sdp=sdp, type=sdp_type)
            connections.add(webrtc_connection)

            # Get answer
            answer = webrtc_connection.get_answer()

            # Modify SDP to include only SHA-256 fingerprint
            modified_sdp = []
            for line in answer["sdp"].splitlines():
                if line.startswith("a=fingerprint:"):
                    if "sha-256" in line:
                        modified_sdp.append(line)
                else:
                    modified_sdp.append(line)
            modified_sdp = "\n".join(modified_sdp)



            # Accept call with answer
            response = await accept_call(phone_number, call_id, modified_sdp)
            if response.status_code != 200:
                logger.error(f"Failed to accept call: {response.text}")
                await webrtc_connection.close()
                connections.discard(webrtc_connection)
                await reject_call(phone_number, call_id, "reject")
                return web.Response(
                    content_type="application/json",
                    text=json.dumps({"error": "Failed to accept call"}),
                    status=500
                )

            logger.info(f"Call setup complete for {phone_number}")
            return web.Response(
                content_type="application/json",
                text=json.dumps({
                    "sdp": answer["sdp"],
                    "type": answer["type"],
                }),
            )

        elif event == "disconnect":
            logger.info(f"Call disconnected from {phone_number}")
            # Cleanup will be handled by connectionstatechange handler
            return web.Response(
                content_type="application/json",
                text=json.dumps({}),
            )

    return web.Response(
        content_type="application/json",
        text=json.dumps({}),
    )

async def on_shutdown(app):
    """Clean up when server shuts down."""
    # Close WebRTC connections
    coros = [conn.close() for conn in connections]
    await asyncio.gather(*coros)
    connections.clear()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WhatsApp call bot")
    parser.add_argument("--host", default="0.0.0.0", help="Host for HTTP server (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=55976, help="Port for HTTP server (default: 55976)")
    parser.add_argument("--verbose", "-v", action="count")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    app = web.Application()
    app.on_shutdown.append(on_shutdown)
    app.router.add_post("/offer", offer)
    web.run_app(app, host=args.host, port=args.port)