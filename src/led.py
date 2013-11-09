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

def send_control(register, data, num_devices=1):
    spi.transfer((register, data) * num_devices)

def interleave(*args):
    for idx in range(0, max(len(arg) for arg in args)):
        for arg in args:
            try:
                yield arg[idx]
            except IndexError:
                continue

def send_data(buf):
    registers = range(1,9)*len(buf)/8
    spi.transfer(interleave(registers, buf))

def brightness(intensity, num_devices=1):
    send_control(MAX7219_REG_INTENSITY, intensity % 16, num_devices)

def init(num_devices=1):
    status = spi.openSPI(speed=1000000)
    print "SPI configuration = ", status

    send_control(MAX7219_REG_SCANLIMIT, 7, num_devices)   # show all 8 digits
    send_control(MAX7219_REG_DECODEMODE, 0, num_devices)  # using a LED matrix (not digits)
    send_control(MAX7219_REG_DISPLAYTEST, 0, num_devices) # no display test
    brightness(7, num_devices)                                 # character intensity: range: 0..15
    send_control(MAX7219_REG_SHUTDOWN, 1, num_devices)    # not in shutdown mode (i.e start it up)
