#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.

import re
import time
import argparse

from luma.led_matrix import legacy
from luma.led_matrix.device import max7219
from luma.core.serial import spi
from luma.core.render import canvas


def demo(n, block_orientation):
    # create matrix device
    serial = spi(port=0, device=0)
    device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation)
    print("Created device")

    # start demo
    msg = "MAX7219 LED Matrix Demo"
    print(msg)
    legacy.show_message(device, msg, fill="white", font=legacy.proportional(legacy.CP437_FONT))
    time.sleep(1)

    msg = "Brightness"
    print(msg)
    legacy.show_message(device, msg, fill="white")

    time.sleep(1)
    with canvas(device) as draw:
        legacy.text(draw, (0, 0), text="A", fill="white")

    time.sleep(1)
    for _ in range(5):
        for intensity in range(16):
            device.contrast(intensity * 16)
            time.sleep(0.1)

    device.contrast(0x80)
    time.sleep(1)

    msg = "Alternative font!"
    print(msg)
    legacy.show_message(device, msg, fill="white", font=legacy.SINCLAIR_FONT)

    time.sleep(1)
    msg = "Proportional font - characters are squeezed together!"
    print(msg)
    legacy.show_message(device, msg, fill="white", font=legacy.proportional(legacy.SINCLAIR_FONT))

    # http://www.squaregear.net/fonts/tiny.shtml
    time.sleep(1)
    msg = "Tiny is, I believe, the smallest possible font \
    (in pixel size). It stands at a lofty four pixels \
    tall (five if you count descenders), yet it still \
    contains all the printable ASCII characters."
    msg = re.sub(" +", " ", msg)
    print(msg)
    legacy.show_message(device, msg, fill="white", font=legacy.proportional(legacy.TINY_FONT))

    time.sleep(1)
    msg = "CP437 Characters"
    print(msg)
    legacy.show_message(device, msg)

    time.sleep(1)
    for x in range(256):
        with canvas(device) as draw:
            legacy.text(draw, (0, 0), text=chr(x), fill="white")
            time.sleep(0.1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='matrix_demo arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', type=str, default='horizontal', choices=['horizontal', 'vertical'], help='Corrects block orientation when wired vertically')

    args = parser.parse_args()

    try:
        demo(args.cascaded, args.block_orientation)
    except KeyboardInterrupt:
        pass
