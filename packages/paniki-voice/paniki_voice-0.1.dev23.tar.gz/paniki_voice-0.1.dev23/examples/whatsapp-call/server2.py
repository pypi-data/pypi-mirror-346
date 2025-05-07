import argparse
import asyncio
import json
import logging
import os
import ssl
import uuid
import requests
import httpx

from aiohttp import web
from av import VideoFrame
from typing import Dict
from bot import run_bot

# from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription, RTCIceServer, RTCConfiguration
# from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRecorder, MediaRelay
# from audio_track_silero import AudioTrack, TTSStreamTrack

from dotenv import load_dotenv
load_dotenv()

from paniki.transports.network.webrtc_connection import IceServer, SmallWebRTCConnection

ROOT = os.path.dirname(__file__)
FBTOKEN = os.getenv("FBTOKEN")
PHONEID = os.getenv("PHONEID")

logger = logging.getLogger("pc")
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

    response = requests.request("POST", url, headers=headers, data=payload)
    
    return response


async def index(request):
    content = open(os.path.join(ROOT, "index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)


async def javascript(request):
    content = open(os.path.join(ROOT, "client.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)


async def offer(request):
    params = await request.json()
    if params.get("messages"):
        return web.Response(
            content_type="application/json",
            text=json.dumps({}),
        )
    if params.get("sdp"):
        session = params
    else:
        call_id = session = params.get("calls")[0]["id"]
        phone_number = session = params.get("calls")[0]["from"]
        session = params.get("calls")[0]["session"]

    # offer = RTCSessionDescription(sdp=session["sdp"], type=session.get("sdp_type") if session.get("sdp_type") else "offer")
    
    # # Define ICE servers (STUN & TURN)
    # ice_servers = [
    #     RTCIceServer(urls="stun:stun.l.google.com:19302"),  # STUN server
    # ]

    # # Create RTC configuration with ICE servers
    # rtc_config = RTCConfiguration(iceServers=ice_servers)

    # pc = RTCPeerConnection(configuration=rtc_config)
    # pc_id = "PeerConnection(%s)" % uuid.uuid4()
    # pcs.add(pc)

    # def log_info(msg, *args):
    #     logger.info(pc_id + " " + msg, *args)

    # log_info("Created for %s", request.remote)

    # # prepare local media
    # # fname = "geely-weekdays-rev1.mp3"
    # fname = "geely-sibuk-rev1.mp3"
    # # fname = "sample-pendek.mp3"
    # player = MediaPlayer(os.path.join(ROOT, fname))
    # # if args.record_to:
    # #     recorder = MediaRecorder(args.record_to)
    # # else:
    #     # recorder = MediaBlackhole()
    # # recorder = MediaRecorder('./record.mp3')

    # @pc.on("datachannel")
    # def on_datachannel(channel):
    #     @channel.on("message")
    #     def on_message(message):
    #         if isinstance(message, str) and message.startswith("ping"):
    #             channel.send("pong" + message[4:])

    # @pc.on("connectionstatechange")
    # async def on_connectionstatechange():
    #     log_info("Connection state is %s", pc.connectionState)
    #     if pc.connectionState == "failed":
    #         await pc.close()
    #         pcs.discard(pc)

    # botAnswerTrack = TTSStreamTrack()
    # @pc.on("track")
    # def on_track(track):
    #     log_info("Track %s received", track.kind)

    #     if track.kind == "audio":
    #         # pc.addTrack(player.audio)
    #         # recorder.addTrack(track)
    #         pc.addTrack(botAnswerTrack)
    #         audio_track = AudioTrack(track, botAnswerTrack)
    #         asyncio.create_task(audio_track.start())

    #     @player.audio.on("ended")
    #     async def audio_ended():
    #         # audio ended, do another process
    #         # await reject_call(phone_number=phone_number, call_id=call_id, action="terminate")
    #         print("audio ended")
    #         # await recorder.stop()

    #     @track.on("ended")
    #     async def on_ended():
    #         log_info("Track %s ended", track.kind)
    #         # await recorder.stop()

    # # handle offer
    # await pc.setRemoteDescription(offer)
    # # await recorder.start()

    # # send answer
    # answer = await pc.createAnswer()
    # print(answer)

    pc_id = phone_number
    if pc_id and pc_id in pcs_map:
        pipecat_connection = pcs_map[pc_id]
        logger.info(f"Reusing existing connection for pc_id: {pc_id}")
        await pipecat_connection.renegotiate(sdp=session["sdp"], type=session.get("sdp_type") if session.get("sdp_type") else "offer")
    else:
        pipecat_connection = SmallWebRTCConnection(ice_servers)
        await pipecat_connection.initialize(sdp=session["sdp"], type=session.get("sdp_type") if session.get("sdp_type") else "offer")

        @pipecat_connection.event_handler("closed")
        async def handle_disconnected(webrtc_connection: SmallWebRTCConnection):
            logger.info(f"Discarding peer connection for pc_id: {webrtc_connection.pc_id}")
            pcs_map.pop(webrtc_connection.pc_id, None)

        #background_tasks.add_task(run_bot, pipecat_connection)
        asyncio.create_task(run_bot(pipecat_connection))

    answer = pipecat_connection.get_answer()

    print('ANSWER : ')
    print(answer)
    # Updating the peer connection inside the map
    pcs_map[answer["pc_id"]] = pipecat_connection
    # Modify the SDP to include only SHA-256 fingerprint
    modified_sdp = []
    for line in answer.get('sdp').splitlines():
        if line.startswith("a=fingerprint:"):
            if "sha-256" in line:
                modified_sdp.append(line)
        else:
            modified_sdp.append(line)
    modified_sdp = "\n".join(modified_sdp)

    #await pc.setLocalDescription(RTCSessionDescription(sdp=modified_sdp, type='answer'))
    
    # accept call
    if PHONEID:
        logger.info("Accepting call")
        response = await accept_call(phone_number=phone_number, call_id=call_id, sdp=modified_sdp)
        logger.info("Call accepted")
        print(response.json())
        if response.status_code != 200:
            #await pc.close()
            await reject_call(phone_number=phone_number, call_id=call_id, action="reject")
            return web.Response(
                content_type="application/json",
                text=json.dumps({
                    "status": "failed"
                }),
            )

    return web.Response(
        content_type="application/json",
        text=json.dumps({
            "sdp": answer.get('sdp'),
            "type": answer.get('type'),
            # "response": response,
        }),
    )


async def on_shutdown(app):
    # close peer connections
    coros = [pc.close() for pc in pcs_map]
    await asyncio.gather(*coros)
    pcs_map.clear()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="WebRTC audio / video / data-channels demo"
    )
    parser.add_argument("--cert-file", help="SSL certificate file (for HTTPS)")
    parser.add_argument("--key-file", help="SSL key file (for HTTPS)")
    parser.add_argument(
        "--host", default="0.0.0.0", help="Host for HTTP server (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", type=int, default=8080, help="Port for HTTP server (default: 8080)"
    )
    parser.add_argument("--record-to", help="Write received media to a file."),
    parser.add_argument("--verbose", "-v", action="count")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.cert_file:
        ssl_context = ssl.SSLContext()
        ssl_context.load_cert_chain(args.cert_file, args.key_file)
    else:
        ssl_context = None

    app = web.Application()
    #app.on_shutdown.append(on_shutdown)
    app.router.add_get("/", index)
    app.router.add_get("/client.js", javascript)
    app.router.add_post("/offer", offer)
    web.run_app(
        app, access_log=None, host=args.host, port=args.port, ssl_context=ssl_context
    )