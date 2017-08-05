#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.

import time
import argparse

from luma.led_matrix.device import max7219, rg_matrix
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT


def demo(w, h, block_orientation, rotate):
    # create matrix device
    #serial = spi(port=0, device=0, gpio=noop())
    #device = max7219(serial, width=w, height=h, rotate=rotate, block_orientation=block_orientation)
    device = rg_matrix(width=w, height=h, rotate=rotate)
    print("Created device")

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="#FF0000", fill="#FF0000")
     #   text(draw, (2, 2), "Hello", fill="#00FF00", font=proportional(LCD_FONT))
     #   text(draw, (2, 10), "World", fill="orange", font=proportional(LCD_FONT))

    time.sleep(300)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='matrix_demo arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--width', type=int, default=8, help='Width')
    parser.add_argument('--height', type=int, default=8, help='height')
    parser.add_argument('--block-orientation', type=int, default=-90, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotation factor')

    args = parser.parse_args()

    try:
        demo(args.width, args.height, args.block_orientation, args.rotate)
    except KeyboardInterrupt:
        pass
