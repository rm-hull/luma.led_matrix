#!/usr/bin/env python
# -*- coding: utf-8 -*-

import spi
import time

from max7219.font import cp437_FONT

MAX7219_REG_NOOP        = 0x0
MAX7219_REG_DIGIT0      = 0x1
MAX7219_REG_DIGIT1      = 0x2
MAX7219_REG_DIGIT2      = 0x3
MAX7219_REG_DIGIT3      = 0x4
MAX7219_REG_DIGIT4      = 0x5
MAX7219_REG_DIGIT5      = 0x6
MAX7219_REG_DIGIT6      = 0x7
MAX7219_REG_DIGIT7      = 0x8
MAX7219_REG_DECODEMODE  = 0x9
MAX7219_REG_INTENSITY   = 0xA
MAX7219_REG_SCANLIMIT   = 0xB
MAX7219_REG_SHUTDOWN    = 0xC
MAX7219_REG_DISPLAYTEST = 0xF

def send_byte(register, data):
    spi.transfer((register, data))

def letter(char, font = cp437_FONT):
    for col in range(8):
        send_byte(col + 1, font[char][col])

def clear():
    for col in range(8):
        send_byte(col + 1, 0)

def show_message(text, transition, font = cp437_FONT):
    prev = ' '
    for curr in text:
        transition(ord(prev), ord(curr), font)
        prev = curr
    transition(ord(prev), 32)

def brightness(intensity):
    send_byte(MAX7219_REG_INTENSITY, intensity % 16)

def init():
    status = spi.openSPI(speed=1000000)
    print "SPI configuration = ", status

    send_byte(MAX7219_REG_SCANLIMIT, 7)   # show all 8 digits
    send_byte(MAX7219_REG_DECODEMODE, 0)  # using a LED matrix (not digits)
    send_byte(MAX7219_REG_DISPLAYTEST, 0) # no display test
    clear()
    brightness(7)                         # character intensity: range: 0..15
    send_byte(MAX7219_REG_SHUTDOWN, 1)    # not in shutdown mode (i.e start it up)
