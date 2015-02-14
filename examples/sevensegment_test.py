#!/usr/bin/env python

import max7219.led as led
import time
import random

display = led.sevensegment(cascaded=3)

for x in range(-30, 128):
    display.write_number(deviceId=0, value=x)
    time.sleep(0.05)

for x in range(99823, 100023):
    display.write_number(deviceId=1, value=x, leftJustify=True)
    time.sleep(0.05)

display.clear(deviceId=1)
time.sleep(1)

display.clear()
time.sleep(1)

a = random.randint(-999, 9999)
b = random.randint(-3223, 9999)

for x in range(500):
    a += random.random() * 10
    b -= 1
    c = a + b / random.random()
    display.write_number(deviceId=0, value=a, decimalPlaces=3)
    display.write_number(deviceId=1, value=b, zeroPad=True)
    display.write_number(deviceId=2, value=c, decimalPlaces=3)
    time.sleep(0.5)
