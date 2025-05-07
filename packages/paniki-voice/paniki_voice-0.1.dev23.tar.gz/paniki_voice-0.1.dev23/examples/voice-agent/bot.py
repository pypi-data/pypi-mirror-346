#
# Copyright (c) 2025, Daily
#
# SPDX-License-Identifier: BSD 2-Clause License
#
import os
import sys

from dotenv import load_dotenv
from loguru import logger

from paniki.audio.vad.silero import SileroVADAnalyzer
from paniki.pipeline.pipeline import Pipeline
from paniki.pipeline.runner import PipelineRunner
from paniki.pipeline.task import PipelineParams, PipelineTask
from paniki.processors.aggregators.openai_llm_context import OpenAILLMContext
from paniki.services.gemini_multimodal_live.gemini import (
    GeminiMultimodalLiveLLMService,
    InputParams,
    GeminiMultimodalModalities
)
from paniki.transports.base_transport import TransportParams
from paniki.transports.network.small_webrtc import SmallWebRTCTransport
from paniki.transcriptions.language import Language

load_dotenv(override=True)

SYSTEM_INSTRUCTION = f"""
"You are Juriko Chatbot, trained to be a friendly by Ibnu, helpful robot.
Your goal is to demonstrate your capabilities in a succinct way.
Your output will be converted to audio so don't include special characters in your answers.
Respond to what the user said in a creative and helpful way. Keep your responses brief. One or two sentences at most.
"""


async def run_bot(webrtc_connection):
    transport = SmallWebRTCTransport(
        webrtc_connection=webrtc_connection,
        params=TransportParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
            vad_analyzer=SileroVADAnalyzer(),
            audio_out_10ms_chunks=2,
        ),
    )

    llm = GeminiMultimodalLiveLLMService(
        api_key=os.getenv("GOOGLE_API_KEY"),
        voice_id="Kore",  # Aoede, Charon, Fenrir, Kore, Puck
        transcribe_user_audio=True,
        transcribe_model_audio=True,
        system_instruction=SYSTEM_INSTRUCTION,
            params=InputParams(
            temperature=0.7,                 # Set model input params
            language=Language.ID_ID,         # Set language (30+ languages supported)
            modalities=GeminiMultimodalModalities.AUDIO  # Response modality
        )
    )

    context = OpenAILLMContext(
        [
            {
                "role": "user",
                "content": "Sapa dengan singkat dan selalu jawab dengan bahasa gaul indonesia",
            }
        ],
    )
    context_aggregator = llm.create_context_aggregator(context)

    pipeline = Pipeline(
        [
            transport.input(),
            context_aggregator.user(),
            llm,  # LLM
            transport.output(),
            context_aggregator.assistant(),
        ]
    )

    task = PipelineTask(
        pipeline,
        params=PipelineParams(
            allow_interruptions=False,
        ),
    )

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        logger.info("Pipecat Client connected")
        # Kick off the conversation.
        await task.queue_frames([context_aggregator.user().get_context_frame()])

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info("Pipecat Client disconnected")

    @transport.event_handler("on_client_closed")
    async def on_client_closed(transport, client):
        logger.info("Pipecat Client closed")
        await task.cancel()

    runner = PipelineRunner(handle_sigint=False)

    await runner.run(task)
