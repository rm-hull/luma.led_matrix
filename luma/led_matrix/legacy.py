# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.

from luma.core.util import deprecation
from luma.core.legacy import text, textsize, show_message  # noqa: F401
from luma.core.legacy.font import proportional, CP437_FONT, SINCLAIR_FONT, LCD_FONT, UKR_FONT, TINY_FONT, DEFAULT_FONT  # noqa: F401


# trigger DeprecationWarning
deprecation_msg = (
    "WARNING! 'luma.led_matrix.legacy' is now deprecated and will be removed in "
    "v1.0.0. Please use the equivalent functionality from "
    "'luma.core.legacy' and 'luma.core.legacy.font'.")
deprecation(deprecation_msg)
