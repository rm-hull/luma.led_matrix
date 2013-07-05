#!/usr/bin/env python

import max7219.led as led
import max7219.canvas as canvas
import time
from random import randrange

led.init()
led.show_message("Hello world!", transition = led.left_scroll)

for x in range(256):
    led.letter(x)
    time.sleep(0.1)

while True:
 #   for x in range(500):
 #       canvas.set_on(randrange(8), randrange(8))
 #       canvas.scroll(randrange(16))
 #       canvas.render()
 #       time.sleep(0.01)

 #   for x in range(500):
 #       canvas.set_off(randrange(8), randrange(8))
 #       canvas.scroll(randrange(16))
 #       canvas.render()
 #       time.sleep(0.01)

    for x in range(500):
        canvas.set_on(4, 4)
        canvas.scroll(randrange(8))
        canvas.render()
        time.sleep(0.01)
