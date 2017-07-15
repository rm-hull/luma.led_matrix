#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.

import time
import colorsys
from luma.led_matrix.device import neosegment
from neopixel_demo import gfx


def rainbow(n=1000, saturation=1, value=1):
    for i in range(n):
        hue = i / float(n)
        color = [int(x * 255) for x in colorsys.hsv_to_rgb(hue, saturation, value)]
        yield ("#%02x%02x%02x" % tuple(color)).upper()


def main():
    sevenseg = neosegment(width=6)
    sevenseg.text = "NEOSEG"
    time.sleep(1)

    for color in rainbow(200):
        sevenseg.set_color(color)
        time.sleep(0.01)

    sevenseg.set_color("white")
    time.sleep(3)

    for _ in range(3):
        for intensity in range(16):
            sevenseg.device.contrast((15 - intensity) * 16)
            time.sleep(0.1)

        for intensity in range(16):
            sevenseg.device.contrast(intensity * 16)
            time.sleep(0.1)

    sevenseg.text = ""
    sevenseg.device.contrast(0x80)
    time.sleep(1)

    sevenseg.text = "rgb"
    time.sleep(1)
    sevenseg.set_char_color(0, "red")
    time.sleep(1)
    sevenseg.set_char_color(1, "green")
    time.sleep(1)
    sevenseg.set_char_color(2, "blue")
    time.sleep(5)

    for _ in range(3):
        for intensity in range(16):
            sevenseg.device.contrast(intensity * 16)
            time.sleep(0.1)

    sevenseg.text = ""
    sevenseg.device.contrast(0x80)
    time.sleep(1)

    gfx(sevenseg.device)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
