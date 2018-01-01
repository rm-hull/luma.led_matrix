#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import time

from luma.led_matrix.device import apa102
from luma.core.render import canvas

device = apa102(width=8, height=1)


def rotate(l):
    return l[-1:] + l[:-1]


def main():
    colors = [
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "indigo",
        "violet",
        "white"
    ]

    for color in colors:
        with canvas(device) as draw:
            draw.line(device.bounding_box, fill=color)
        time.sleep(2)

    device.contrast(0x30)
    for _ in range(80):
        with canvas(device) as draw:
            for x, color in enumerate(colors):
                draw.point((x, 0), fill=color)

        colors = rotate(colors)
        time.sleep(0.2)

    time.sleep(4)

    device.contrast(0x80)
    time.sleep(1)
    device.contrast(0x10)
    time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
