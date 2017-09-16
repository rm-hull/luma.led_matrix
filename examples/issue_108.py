#!usr/bin/env python

import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text

print('Press Ctrl-C to quit...')

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=5, block_orientation=0)

currentLoop = 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='matrix_demo arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=5, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')

    args = parser.parse_args()

    while True:

        currentLoop = currentLoop + 1

        Tv = str(currentLoop)
        Tv = Tv.rjust(5, " ")

        with canvas(device) as draw:
            text(draw, (0, 0), Tv, fill="white")

        print(Tv)
        time.sleep(1)

        if currentLoop >= 99999:
            currentLoop = 0
