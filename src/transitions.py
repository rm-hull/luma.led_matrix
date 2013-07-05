#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

from max7219.led import send_byte
from max7219.font import cp437_FONT

def up_scroll(from_char, to_char, font = cp437_FONT):
    for i in range(7,-1,-1):
        time.sleep(0.1)
        for col in range(8):
            data = (font[from_char][col] >> (8 - i) | font[to_char][col] << i) & 0xFF
            send_byte(col + 1, data)

def left_scroll(from_char, to_char, font = cp437_FONT):
    for i in range(8):
        time.sleep(0.1)
        for col in range(8):
            if col + i < 8:
                data = font[from_char][col + i]
            else:
                data = font[to_char][col + i - 8]

            send_byte(col + 1, data)

def simple(from_char, to_char, font = cp437_FONT):
    letter(to_char, font)
    time.sleep(0.25)
    # Clear between letters
    letter(0, font)
    time.sleep(0.01)
