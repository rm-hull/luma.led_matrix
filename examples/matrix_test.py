#!/usr/bin/env python

import max7219.led as led
import time
from max7219.font import proportional, SINCLAIR_FONT
from random import randrange

device = led.matrix(cascaded=1)

device.show_message("MAX7219 LED Matrix Demo")


time.sleep(1)
device.show_message("Brightness")

time.sleep(1)
device.letter(0, ord('A'))
time.sleep(1)
for _ in range(5):
    for intensity in xrange(16):
        device.brightness(intensity)
        time.sleep(0.1)

device.brightness(7)

time.sleep(1)
device.show_message("Orientation")

time.sleep(1)
device.letter(0, ord('A'))
time.sleep(1)
for _ in range(5):
    for angle in [0, 90, 180, 270]:
        device.orientation(angle)
        time.sleep(0.2)

device.orientation(0)
time.sleep(1)

device.show_message("Inverse")
time.sleep(1)
device.letter(0, ord('A'))
time.sleep(1)
for _ in range(10):
    device.invert(1)
    time.sleep(0.25)
    device.invert(0)
    time.sleep(0.25)

time.sleep(1)
device.show_message("Alternative font!", font=SINCLAIR_FONT)

time.sleep(1)
device.show_message("Proportional font - characters are squeezed together!", font=proportional(SINCLAIR_FONT))

time.sleep(1)
device.show_message("CP437 Characters")

time.sleep(1)
for x in range(256):
#    device.letter(1, 32 + (x % 64))
    device.letter(0, x)
    time.sleep(0.1)

time.sleep(1)
device.show_message("Scrolling and pixel setting...")

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
