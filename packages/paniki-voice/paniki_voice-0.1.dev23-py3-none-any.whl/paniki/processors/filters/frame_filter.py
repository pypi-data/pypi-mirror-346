#
# Copyright (c) 2024–2025, Paniki
#
# SPDX-License-Identifier: BSD 2-Clause License
#

from typing import Tuple, Type

from paniki.frames.frames import EndFrame, Frame, SystemFrame
from paniki.processors.frame_processor import FrameDirection, FrameProcessor


class FrameFilter(FrameProcessor):
    def __init__(self, types: Tuple[Type[Frame], ...]):
        super().__init__()
        self._types = types

    #
    # Frame processor
    #

    def _should_passthrough_frame(self, frame):
        if isinstance(frame, self._types):
            return True

        return isinstance(frame, (EndFrame, SystemFrame))

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)

        if self._should_passthrough_frame(frame):
            await self.push_frame(frame, direction)
