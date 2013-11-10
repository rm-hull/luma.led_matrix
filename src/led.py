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

def send_control(register, data):
    spi.transfer((register, data))

def interleave(*args):
    for idx in range(0, max(len(arg) for arg in args)):
        for arg in args:
            try:
                yield arg[idx]
            except IndexError:
                continue

def send_data(buf):
    devices = len(buf) / 8
    for col in range(8):
        registers =  [0] * (devices - 1) + [col + 1]
        #registers =  [col + 1] * devices
        data = [buf[x + col] for x in range(0, devices * 8, 8)]
        #print(tuple(interleave(registers, data)))
        spi.transfer(tuple(interleave(registers, data)))

def brightness(intensity):
    send_control(MAX7219_REG_INTENSITY, intensity % 16)

def init():
    status = spi.openSPI(device="/dev/spidev0.0", speed=1000000, delay=0)
    print "SPI configuration = ", status

    send_control(MAX7219_REG_SCANLIMIT, 7 )   # show all 8 digits
    send_control(MAX7219_REG_DECODEMODE, 0)  # using a LED matrix (not digits)
    send_control(MAX7219_REG_DISPLAYTEST, 0) # no display test
    brightness(7)                                 # character intensity: range: 0..15
    send_control(MAX7219_REG_SHUTDOWN, 1)    # not in shutdown mode (i.e start it up)
