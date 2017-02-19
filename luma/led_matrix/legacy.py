# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.

# FIXME: To be removed when 0.6.0 released

from luma.core.legacy import text, textsize, show_message
from luma.core.legacy.font import proportional, CP437_FONT, SINCLAIR_FONT, \
    LCD_FONT, UKR_FONT, TINY_FONT, DEFAULT_FONT

print("\nWARNING! 'luma.led_matrix.legacy' is now deprecated and will be removed in\n"
      "         the next major release. Please use the equivalent functionality from\n"
      "         'luma.core.legacy' and 'luma.core.legacy.font'.\n")

text
textsize
show_message
proportional
CP437_FONT
SINCLAIR_FONT
LCD_FONT
UKR_FONT
TINY_FONT
DEFAULT_FONT
