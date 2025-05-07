#
# Copyright (c) 2024–2025, Paniki
#
# SPDX-License-Identifier: BSD 2-Clause License
#

from importlib.metadata import version

from loguru import logger

__version__ = version("paniki-voice")

logger.info(f"Paniki Voice {__version__}")
