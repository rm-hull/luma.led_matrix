#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Example for seven segment displays.
"""

import time
from datetime import datetime

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment


def date(seg):
    """
    Display current date on device.
    """
    now = datetime.now()
    seg.text = now.strftime("%y-%m-%d")


def clock(seg, seconds):
    """
    Display current time on device.
    """
    interval = 0.5
    for i in range(int(seconds / interval)):
        now = datetime.now()
        seg.text = now.strftime("%H-%M-%S")

        # calculate blinking dot
        if i % 2 == 0:
            seg.text = now.strftime("%H-%M-%S")
        else:
            seg.text = now.strftime("%H %M %S")

        time.sleep(interval)


def show_message_vp(device, msg, delay=0.1):
    # Implemented with virtual viewport
    width = device.width
    padding = " " * width
    msg = padding + msg + padding
    n = len(msg)

    virtual = viewport(device, width=n, height=8)
    sevensegment(virtual).text = msg
    for i in reversed(list(range(n - width))):
        virtual.set_position((i, 0))
        time.sleep(delay)


def show_message_alt(seg, msg, delay=0.1):
    # Does same as above but does string slicing itself
    width = seg.device.width
    padding = " " * width
    msg = padding + msg + padding

    for i in range(len(msg)):
        seg.text = msg[i:i + width]
        time.sleep(delay)


def main():
    # create seven segment device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=1)
    seg = sevensegment(device)

    print('Simple text...')
    for _ in range(8):
        seg.text = "HELLO"
        time.sleep(0.6)
        seg.text = " GOODBYE"
        time.sleep(0.6)

    # Digit slicing
    print("Digit slicing")
    seg.text = "_" * seg.device.width
    time.sleep(1.0)

    for i, ch in enumerate([9, 8, 7, 6, 5, 4, 3, 2]):
        seg.text[i] = str(ch)
        time.sleep(0.6)

    for i in range(len(seg.text)):
        del seg.text[0]
        time.sleep(0.6)

    # Scrolling Alphabet Text
    print('Scrolling alphabet text...')
    show_message_vp(device, "HELLO EVERYONE!")
    show_message_vp(device, "PI is 3.14159 ... ")
    show_message_vp(device, "IP is 127.0.0.1 ... ")
    show_message_alt(seg, "0123456789 abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    # Digit futzing
    date(seg)
    time.sleep(5)
    clock(seg, seconds=10)

    # Brightness
    print('Brightness...')
    for x in range(5):
        for intensity in range(16):
            seg.device.contrast(intensity * 16)
            time.sleep(0.1)
    device.contrast(0x7F)


if __name__ == '__main__':
    main()
