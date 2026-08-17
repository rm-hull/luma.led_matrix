#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2026 Richard Hull and contributors
# See LICENSE.rst for details.

import time

from luma.led_matrix.device import scrollphathd
from luma.core.render import canvas

device = scrollphathd()


def main():
    # Sweep a single lit pixel across the whole 17x7 grid
    for y in range(device.height):
        for x in range(device.width):
            with canvas(device) as draw:
                draw.point((x, y), fill="white")
            time.sleep(0.02)

    # Fade the whole display up and down using the alpha channel to
    # control per-pixel brightness
    for _ in range(3):
        for alpha in list(range(0, 256, 8)) + list(range(255, -1, -8)):
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, fill=(255, 255, 255, alpha))
            time.sleep(0.01)

    device.clear()
    device.show()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
