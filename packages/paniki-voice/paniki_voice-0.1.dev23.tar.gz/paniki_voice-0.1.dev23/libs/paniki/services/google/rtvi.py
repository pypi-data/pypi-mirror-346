#
# Copyright (c) 2024–2025, Paniki
#
# SPDX-License-Identifier: BSD 2-Clause License
#

from typing import List, Literal, Optional

from pydantic import BaseModel

from paniki.frames.frames import Frame
from paniki.processors.frame_processor import FrameDirection, FrameProcessor
from paniki.processors.frameworks.rtvi import RTVIObserver
from paniki.services.google.frames import LLMSearchOrigin, LLMSearchResponseFrame


class RTVISearchResponseMessageData(BaseModel):
    search_result: Optional[str]
    rendered_content: Optional[str]
    origins: List[LLMSearchOrigin]


class RTVIBotLLMSearchResponseMessage(BaseModel):
    label: Literal["rtvi-ai"] = "rtvi-ai"
    type: Literal["bot-llm-search-response"] = "bot-llm-search-response"
    data: RTVISearchResponseMessageData


class GoogleRTVIObserver(RTVIObserver):
    def __init__(self, rtvi: FrameProcessor):
        super().__init__(rtvi)

    async def on_push_frame(
        self,
        src: FrameProcessor,
        dst: FrameProcessor,
        frame: Frame,
        direction: FrameDirection,
        timestamp: int,
    ):
        await super().on_push_frame(src, dst, frame, direction, timestamp)

        if isinstance(frame, LLMSearchResponseFrame):
            await self._handle_llm_search_response_frame(frame)

    async def _handle_llm_search_response_frame(self, frame: LLMSearchResponseFrame):
        message = RTVIBotLLMSearchResponseMessage(
            data=RTVISearchResponseMessageData(
                search_result=frame.search_result,
                origins=frame.origins,
                rendered_content=frame.rendered_content,
            )
        )
        await self.push_transport_message_urgent(message)
