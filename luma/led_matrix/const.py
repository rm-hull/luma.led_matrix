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


class is31fl3731(object):
    NUM_FRAMES = 8
    NUM_PIXELS = 144

    # The "function" registers (mode, frame select, shutdown, etc) all live
    # in a reserved configuration bank, selected the same way as any other
    # frame.
    CONFIG_BANK = 0x0B
    BANK_ADDRESS = 0xFD

    MODE = 0x00
    FRAME = 0x01
    AUDIOSYNC = 0x06
    SHUTDOWN = 0x0A

    PICTURE_MODE = 0x00

    # Within a frame, the first 18 bytes (144 bits) are a bitmap of which
    # LED positions are physically wired up and should be lit; the PWM
    # brightness values for those same 144 positions follow on immediately
    # afterwards.
    LED_ENABLE = 0x00
    LED_PWM = 0x24
