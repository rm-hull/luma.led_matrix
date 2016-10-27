#!/usr/bin/env python3

"""
Async example for seven segment displays.
Note: this only works on Python3
"""

import asyncio
import max7219.led as led

def main():
    loop = asyncio.get_event_loop()
    device = led.sevensegment()

    device.show_message("HELLO EVERYONE!", event_loop=loop)

    try:
        loop.run_forever()
    finally:
        loop.close()

if __name__ == '__main__':
    main()
