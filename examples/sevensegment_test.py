#!/usr/bin/env python

import max7219.led as led
import time
import random
from datetime import datetime

def date(device, deviceId):

    now = datetime.now()
    day = now.day
    month = now.month
    year = now.year - 2000

    # Set day
    device.letter(deviceId, 8, int(day / 10))     # Tens
    device.letter(deviceId, 7, day % 10)          # Ones
    device.letter(deviceId, 6, '-')               # dash
    # Set day
    device.letter(deviceId, 5, int(month / 10))     # Tens
    device.letter(deviceId, 4, month % 10)     # Ones
    device.letter(deviceId, 3, '-')               # dash
    # Set day
    device.letter(deviceId, 2, int(year / 10))     # Tens
    device.letter(deviceId, 1, year % 10)     # Ones


def clock(device, deviceId, seconds):

    for _ in xrange(seconds):
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second
        dot = second % 2 == 0                # calculate blinking dot
        # Set hours
        device.letter(deviceId, 4, int(hour / 10))     # Tens
        device.letter(deviceId, 3, hour % 10, dot)     # Ones
        # Set minutes
        device.letter(deviceId, 2, int(minute / 10))   # Tens
        device.letter(deviceId, 1, minute % 10)        # Ones
        time.sleep(1)


device = led.sevensegment(cascaded=3)

for _ in range(8):
    device.write_text(0, "HELLO")
    time.sleep(0.6)
    device.write_text(0, " GOODBYE")
    time.sleep(0.6)

# Scrolling Alphabet Text
device.show_message("HELLO EVERYONE!")
device.show_message("0123456789 abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# Digit futzing
date(device, 1)
clock(device, 0, seconds=10)

# Brightness
for x in xrange(5):
    for intensity in xrange(16):
        device.brightness(intensity)
        time.sleep(0.1)
device.brightness(7)

# Scrolling
for x in xrange(2):
    for _ in xrange(8):
        device.scroll_right()
        time.sleep(0.1)
    time.sleep(1)
device.clear()

# Negative numbers
for x in range(-30, 128):
    device.write_number(deviceId=0, value=x)
    time.sleep(0.05)

# Hex numbers
for x in range(0xfa909, 0xfab2a):
    device.write_number(deviceId=1, value=x, base=16, leftJustify=True)
    time.sleep(0.025)

device.clear(deviceId=1)
time.sleep(1)

device.clear()
time.sleep(1)

a = random.randint(-999, 999)
b = random.randint(-3223, 999)

device.brightness(3)
for x in range(500):
    a += random.random() * 10
    b -= 1
    c = a + b / (random.random() * 43)
    device.write_number(deviceId=0, value=a, decimalPlaces=1)
    device.write_number(deviceId=1, value=b, zeroPad=True)
    device.write_number(deviceId=2, value=c, decimalPlaces=2)
    time.sleep(0.5)
