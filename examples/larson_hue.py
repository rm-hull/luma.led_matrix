#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.
#
# Based on https://github.com/pimoroni/blinkt/blob/master/examples/larson_hue.py

import math
import time
import colorsys

from luma.led_matrix.device import apa102
from luma.core.render import canvas

device = apa102(width=8, height=1)

FALLOFF = 1.9
SCAN_SPEED = 4


def main():

    start_time = time.time()

    while True:
        delta = (time.time() - start_time)

        # Offset is a sine wave derived from the time delta
        # we use this to animate both the hue and larson scan
        # so they are kept in sync with each other
        offset = (math.sin(delta * SCAN_SPEED) + 1) / 2

        # Use offset to pick the right colour from the hue wheel
        hue = int(round(offset * 360))

        # Now we generate a value from 0 to 7
        offset = int(round(offset * 7))

        with canvas(device) as draw:
            for x in range(8):
                sat = 1.0

                val = 7 - (abs(offset - x) * FALLOFF)
                val /= 7.0  # Convert to 0.0 to 1.0
                val = max(val, 0.0)  # Ditch negative values

                xhue = hue  # Grab hue for this pixel
                xhue += (1 - val) * 10  # Use the val offset to give a slight colour trail variation
                xhue %= 360  # Clamp to 0-359
                xhue /= 360.0  # Convert to 0.0 to 1.0

                r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(xhue, sat, val)]

                draw.point((x, 0), fill=(r, g, b, int(val * 256)))

        time.sleep(0.001)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
