#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.

import time

import luma.led_matrix.legacy as legacy
from luma.led_matrix.device import max7219
from luma.core.serial import spi
from luma.core.render import canvas


def demo():
    # create matrix device
    serial = spi(port=0, device=0)
    device = max7219(serial, cascaded=2)
    print("Created device")

    # start demo
    msg = "MAX7219 LED Matrix Demo"
    print(msg)
    legacy.show_message(device, msg, font=legacy.proportional(legacy.CP437_FONT))
    time.sleep(1)

    msg = "Brightness"
    print(msg)
    legacy.show_message(device, msg)

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
    legacy.show_message(device, msg, font=legacy.SINCLAIR_FONT)

    time.sleep(1)
    msg = "Proportional font - characters are squeezed together!"
    print(msg)
    legacy.show_message(device, msg, font=legacy.proportional(legacy.SINCLAIR_FONT))

    # http://www.squaregear.net/fonts/tiny.shtml
    time.sleep(1)
    msg = "Tiny is, I believe, the smallest possible font \
    (in pixel size). It stands at a lofty four pixels \
    tall (five if you count descenders), yet it still \
    contains all the printable ASCII characters."
    print(msg)
    legacy.show_message(device, msg, font=legacy.proportional(legacy.TINY_FONT))

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
    demo()
