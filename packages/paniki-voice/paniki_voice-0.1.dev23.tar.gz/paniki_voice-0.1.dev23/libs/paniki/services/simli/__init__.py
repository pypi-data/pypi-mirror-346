#
# Copyright (c) 2024–2025, Paniki
#
# SPDX-License-Identifier: BSD 2-Clause License
#

import sys

from paniki.services import DeprecatedModuleProxy

from .video import *

sys.modules[__name__] = DeprecatedModuleProxy(globals(), "simli", "simli.video")
