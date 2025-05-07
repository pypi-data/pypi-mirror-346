#
# Copyright (c) 2024–2025, Paniki
#
# SPDX-License-Identifier: BSD 2-Clause License
#

import sys

from paniki.services import DeprecatedModuleProxy

from .ai_service import *
from .image_service import *
from .llm_service import *
from .stt_service import *
from .tts_service import *
from .vision_service import *

sys.modules[__name__] = DeprecatedModuleProxy(
    globals(),
    "ai_services",
    "ai_service.[image_service,llm_service,stt_service,tts_service,vision_service]",
)
