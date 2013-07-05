#!/usr/bin/env python
# -*- coding: utf-8 -*-

from max7219.led import send_byte
from max7219.font import cp437_FONT

gfxbuf = [0,0,0,0,0,0,0,0]

def letter(char, font = cp437_FONT):
    for col in range(8):
        gfxbuf[col] = font[char][col]

def clear():
    for col in range(8):
        gfxbuf[col] = 0

def render():
    for col in range(8):
        send_byte(col + 1, gfxbuf[col])

def set_on(x, y):
    gfxbuf[y] = gfxbuf[y] | (1 << x)

def set_off(x, y):
    gfxbuf[y] = gfxbuf[y] & ~(1 << x)

def scroll(direction):
    if direction == 0:  # UP
        for col in range(8):
            gfxbuf[col] >>= 1

    elif direction == 2: # RIGHT
        gfxbuf[0] = 0
        for col in range(6,-1,-1):
            gfxbuf[col+1] = gfxbuf[col]

    elif direction == 4: # DOWN
        for col in range(8):
            gfxbuf[col] <<= 1

    elif direction == 6: # LEFT
        for col in range(1,8):
            gfxbuf[col-1] = gfxbuf[col]
        gfxbuf[7] = 0

    elif direction < 8:  # DIAGONALS
        scroll(direction % 8 - 1)
        scroll(direction % 8 + 1)