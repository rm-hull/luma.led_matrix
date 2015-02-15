#!/usr/bin/env python

import max7219.led as led
import time
from random import randrange

device = led.matrix(cascaded=1)
device.show_message("Hello world!")

for x in range(256):
#    device.letter(1, 32 + (x % 64))
    device.letter(0, x)
    time.sleep(0.1)

while True:
    for x in range(500):
        device.pixel(4, 4, 1, redraw=False)
        direction = randrange(8)
        if direction == 7 or direction == 0 or direction == 1:
            device.scroll_up(redraw=False)
        if direction == 1 or direction == 2 or direction == 3:
            device.scroll_right(redraw=False)
        if direction == 3 or direction == 4 or direction == 5:
            device.scroll_down(redraw=False)
        if direction == 5 or direction == 6 or direction == 7:
            device.scroll_left(redraw=False)

        device.flush()
        time.sleep(0.01)
