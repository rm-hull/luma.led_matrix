#!/usr/bin/env python

import time
from random import randrange

import max7219.led as led
from max7219.font import proportional, SINCLAIR_FONT, TINY_FONT, CP437_FONT


# create matrix device
device = led.matrix(cascaded=1)

msg = "MAX7219 LED Matrix Demo"
print(msg)
device.show_message(msg, font=proportional(CP437_FONT))
time.sleep(1)

msg = "Brightness"
print(msg)
device.show_message(msg)

time.sleep(1)
device.letter(0, ord('A'))
time.sleep(1)
for _ in range(5):
    for intensity in range(16):
        device.brightness(intensity)
        time.sleep(0.1)

device.brightness(7)
time.sleep(1)

msg = "Orientation"
print(msg)
device.show_message(msg)
time.sleep(1)

device.letter(0, ord('A'))
time.sleep(1)
for _ in range(5):
    for angle in [0, 90, 180, 270]:
        device.orientation(angle)
        time.sleep(0.2)

for row in range(8):
    device.scroll_down()
    time.sleep(0.2)

device.orientation(0)
time.sleep(1)

msg = "Inverse"
print(msg)
device.show_message(msg)
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

# http://www.squaregear.net/fonts/tiny.shtml
time.sleep(1)
device.show_message(
"Tiny is, I believe, the smallest possible font \
(in pixel size). It stands at a lofty four pixels \
tall (five if you count descenders), yet it still \
contains all the printable ASCII characters.",
font=proportional(TINY_FONT))

time.sleep(1)
msg = "CP437 Characters"
print(msg)
device.show_message(msg)

time.sleep(1)
for x in range(256):
#    device.letter(1, 32 + (x % 64))
    device.letter(0, x)
    time.sleep(0.1)

time.sleep(1)
msg = "Scrolling and pixel setting..."
print(msg)
device.show_message(msg)

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
