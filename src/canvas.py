#!/usr/bin/env python
# -*- coding: utf-8 -*-

import max7219.led as led
import max7219.font as font

def init(num_devices):
    global gfxbuf
    led.init()
    gfxbuf = [0] * 8 * num_devices

def letter(char, device=0, font=font.cp437_FONT):
    for col in range(8):
        gfxbuf[col + (device * 8)] = font[char][col]

def clear(device=0):
    letter(' ', device)

def render():
    led.send_data(gfxbuf)

def set_on(x, y):
    gfxbuf[y] = gfxbuf[y] | (1 << x)

def set_off(x, y):
    gfxbuf[y] = gfxbuf[y] & ~(1 << x)

def scroll(direction):
    if direction == 0:  # UP
        for col in range(len(gfxlen)):
            gfxbuf[col] >>= 1

    elif direction == 2: # RIGHT
        gfxbuf[0] = 0
        for col in range(len(gfxbuf)-2,-1,-1):
            gfxbuf[col+1] = gfxbuf[col]

    elif direction == 4: # DOWN
        for col in range(len(gfxbuf)):
            gfxbuf[col] <<= 1

    elif direction == 6: # LEFT
        for col in range(1,len(gfxbuf)):
            gfxbuf[col-1] = gfxbuf[col]
        gfxbuf[len(gfxbuf)-1] = 0

    elif direction < 8:  # DIAGONALS
        scroll(direction % 8 - 1)
        scroll(direction % 8 + 1)