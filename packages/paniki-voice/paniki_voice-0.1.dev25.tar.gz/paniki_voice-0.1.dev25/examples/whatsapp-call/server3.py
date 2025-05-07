import argparse
import asyncio
import sys
import os
import json
import httpx
from contextlib import asynccontextmanager
from typing import Dict

import uvicorn
from bot import run_bot
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import FileResponse
from loguru import logger

from paniki.transports.network.webrtc_connection import IceServer, SmallWebRTCConnection

# Load environment variables
load_dotenv(override=True)

FBTOKEN = os.getenv("FBTOKEN")
PHONEID = os.getenv("PHONEID")

app = FastAPI()

# Store connections by pc_id
pcs_map: Dict[str, SmallWebRTCConnection] = {}


ice_servers = [
    IceServer(
        urls="stun:stun.l.google.com:19302",
    )
]

async def accept_call(phone_number, call_id, sdp):
    url = f"https://graph.facebook.com/v18.0/{PHONEID}/calls"

    payload = json.dumps({
        "to": phone_number,
        "messaging_product": "whatsapp",
        "call_id": call_id,
        "action": "accept",
        "session": {
            "sdp": sdp,
            "sdp_type": "answer"
        }
    })
    logger.info(f"Send request to {url} with payload {payload}")
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {FBTOKEN}",
    }

    # response = requests.request("POST", url, headers=headers, data=payload)
    response = httpx.post(url=url, headers=headers, data=payload)
    logger.info(f"Got response")
    
    return response

async def reject_call(phone_number, call_id, action):
    url = f"https://graph.facebook.com/v18.0/{PHONEID}/calls"

    payload = json.dumps({
        "to": phone_number,
        "messaging_product": "whatsapp",
        "call_id": call_id,
        "action": action
    })
    print(payload)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {FBTOKEN}",
        'Cookie': 'ps_l=1; ps_n=1'
    }

    response = httpx.post(url, headers=headers, data=payload)
    
    return response


@app.post("/offer")
async def offer(request: dict, background_tasks: BackgroundTasks):
    params = request

    if params.get("messages"):
        return {}
    
    if params.get("sdp"):
        session = params
    else:
        call_id = params.get("calls")[0]["id"]
        phone_number = params.get("calls")[0]["from"]
        session = params.get("calls")[0]["session"]
        
    pc_id = session.get("pc_id")

    logger.info(f"Session {session}")

    if pc_id and pc_id in pcs_map:
        paniki_connection = pcs_map[pc_id]
        logger.info(f"Reusing existing connection for pc_id: {pc_id}")
        await paniki_connection.renegotiate(sdp=session["sdp"], type=session["sdp_type"])
    else:
        paniki_connection = SmallWebRTCConnection(ice_servers)
        await paniki_connection.initialize(sdp=session["sdp"], type=session["sdp_type"])

        @paniki_connection.event_handler("closed")
        async def handle_disconnected(webrtc_connection: SmallWebRTCConnection):
            logger.info(f"Discarding peer connection for pc_id: {webrtc_connection.pc_id}")
            pcs_map.pop(webrtc_connection.pc_id, None)

        background_tasks.add_task(run_bot, paniki_connection)

    answer = paniki_connection.get_answer()

    logger.info(f"Answer {answer}")
    # Updating the peer connection inside the map
    pcs_map[answer["pc_id"]] = paniki_connection

    # Modify the SDP to include only SHA-256 fingerprint
    modified_sdp = []
    for line in answer.get('sdp').splitlines():
        if line.startswith("a=fingerprint:"):
            if "sha-256" in line:
                modified_sdp.append(line)
        else:
            modified_sdp.append(line)
    modified_sdp = "\n".join(modified_sdp)

    if PHONEID:
        logger.info("Accepting call")
        response = await accept_call(phone_number=phone_number, call_id=call_id, sdp=modified_sdp)
        logger.info("Call accepted")
        print(response.json())
        if response.status_code != 200:
            await reject_call(phone_number=phone_number, call_id=call_id, action="reject")
            return {"status": "failed"}

    return answer


@app.get("/")
async def serve_index():
    return FileResponse("index.html")


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield  # Run app
    coros = [pc.close() for pc in pcs_map.values()]
    await asyncio.gather(*coros)
    pcs_map.clear()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebRTC demo")
    parser.add_argument(
        "--host", default="localhost", help="Host for HTTP server (default: localhost)"
    )
    parser.add_argument(
        "--port", type=int, default=8080, help="Port for HTTP server (default: 8080)"
    )
    parser.add_argument("--verbose", "-v", action="count")
    args = parser.parse_args()

    logger.remove(0)
    if args.verbose:
        logger.add(sys.stderr, level="TRACE")
    else:
        logger.add(sys.stderr, level="DEBUG")

    uvicorn.run(app, host=args.host, port=args.port)
