#
# Copyright (c) 2024–2025, Paniki
#
# SPDX-License-Identifier: BSD 2-Clause License
#

from abc import abstractmethod
from typing import List

from paniki.processors.frame_processor import FrameProcessor


class BasePipeline(FrameProcessor):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def processors_with_metrics(self) -> List[FrameProcessor]:
        pass
