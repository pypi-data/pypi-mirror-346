#
# Copyright (c) 2024–2025, Paniki
#
# SPDX-License-Identifier: BSD 2-Clause License
#

from paniki.frames.frames import EndFrame, Frame, SystemFrame
from paniki.processors.frame_processor import FrameDirection, FrameProcessor


class NullFilter(FrameProcessor):
    """This filter doesn't allow passing any frames up or downstream."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    #
    # Frame processor
    #

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)

        if isinstance(frame, (SystemFrame, EndFrame)):
            await self.push_frame(frame, direction)
