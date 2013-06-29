#!/usr/bin/env python

import max7219.led as led
import time

led.init()
led.show_message("Hello world!", transition = led.left_scroll)

for x in range(256):
    led.letter(x)
    time.sleep(0.15)
