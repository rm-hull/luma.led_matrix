#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import time
import random
import colorsys
from luma.led_matrix.device import neosegment
from neopixel_demo import gfx


def rainbow(n=1000, saturation=1, value=1):
    """
    A generator that yields 'n' hues from the rainbow in the hex format #RRGGBB.
    By default the saturation and value (from HSV) are both set to 1.
    """
    for i in range(n):
        hue = i / float(n)
        color = [int(x * 255) for x in colorsys.hsv_to_rgb(hue, saturation, value)]
        yield ("#%02x%02x%02x" % tuple(color)).upper()


def main():
    neoseg = neosegment(width=6)
    neoseg.text = "NEOSEG"
    time.sleep(1)
    neoseg.color[0] = "yellow"
    time.sleep(1)
    neoseg.color[3:5] = ["blue", "orange"]
    time.sleep(1)
    neoseg.color = "white"
    time.sleep(1)

    for _ in range(10):
        neoseg.device.hide()
        time.sleep(0.1)
        neoseg.device.show()
        time.sleep(0.1)

    time.sleep(1)

    for color in rainbow(200):
        neoseg.color = color
        time.sleep(0.01)

    colors = list(rainbow(neoseg.device.width))
    for _ in range(50):
        random.shuffle(colors)
        neoseg.color = colors
        time.sleep(0.1)

    neoseg.color = "white"
    time.sleep(3)

    for _ in range(3):
        for intensity in range(16):
            neoseg.device.contrast((15 - intensity) * 16)
            time.sleep(0.1)

        for intensity in range(16):
            neoseg.device.contrast(intensity * 16)
            time.sleep(0.1)

    neoseg.text = ""
    neoseg.device.contrast(0x80)
    time.sleep(1)

    neoseg.text = "rgb"
    time.sleep(1)
    neoseg.color[0] = "red"
    time.sleep(1)
    neoseg.color[1] = "green"
    time.sleep(1)
    neoseg.color[2] = "blue"
    time.sleep(5)

    for _ in range(3):
        for intensity in range(16):
            neoseg.device.contrast(intensity * 16)
            time.sleep(0.1)

    neoseg.text = ""
    neoseg.device.contrast(0x80)
    time.sleep(1)

    gfx(neoseg.device)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
