# -*- coding: utf-8 -*-
# Copyright (c) 2013-18 Richard Hull and contributors
# See LICENSE.rst for details.


class max7219(object):
    NOOP = 0x00
    DIGIT_0 = 0x01
    DECODEMODE = 0x09
    INTENSITY = 0x0A
    SCANLIMIT = 0x0B
    SHUTDOWN = 0x0C
    DISPLAYTEST = 0x0F
