# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.

# Example usage:
#
#   from luma.core.serial import spi
#   from luma.core.render import canvas
#   from luma.led_matrix.device import max7219
#   from PIL import ImageDraw
#
#   serial = spi(port=0, device=0)
#   device = max7219(serial, cascaded=2)
#
#   with canvas(device) as draw:
#      draw.rectangle(device.bounding_box, outline="white", fill="black")
#
# As soon as the with-block scope level is complete, the graphics primitives
# will be flushed to the device.
#
# Creating a new canvas is effectively 'carte blanche': If you want to retain
# an existing canvas, then make a reference like:
#
#    c = canvas(device)
#    for X in ...:
#        with c as draw:
#            draw.rectangle(...)
#
# As before, as soon as the with block completes, the canvas buffer is flushed
# to the device

from luma.core.device import device
import luma.core.error
import luma.led_matrix.const


class max7219(device):
    """
    Encapsulates the serial interface to a series of 8x8 LED matrixes
    daisychained together with MAX7219 chips. On creation, an initialization
    sequence is pumped to the display to properly configure it. Further control
    commands can then be called to affect the brightness and other settings.
    """
    def __init__(self, serial_interface=None, width=8, height=8, rotate=0):
        super(max7219, self).__init__(luma.led_matrix.const.max7219, serial_interface)
        self.capabilities(width, height, rotate)

        if width % 8 != 0 or height != 8:
            raise luma.core.error.DeviceDisplayModeError(
                "Unsupported display mode: {0} x {1}".format(width, height))

        self.cascaded = width // 8

        self.data([self._const.SCANLIMIT, 7] * self.cascaded)
        self.data([self._const.DECODEMODE, 0] * self.cascaded)
        self.data([self._const.DISPLAYTEST, 0] * self.cascaded)

        self.contrast(0x70)
        self.clear()
        self.show()

    def display(self, image):
        """
        Takes a 1-bit :py:mod:`PIL.Image` and dumps it to the LED matrix display
        via the MAX7219 serializers.
        """
        assert(image.mode == self.mode)
        assert(image.size == self.size)

        image = self.preprocess(image)

        for digit in range(8):
            buf = []
            for daisychained_device in reversed(range(self.cascaded)):
                byte = 0
                for y in range(self._h):
                    x = (daisychained_device * 8) + digit
                    pixel = image.getpixel((x, y))
                    if pixel > 0:
                        byte |= 1 << y

                buf += [digit + self._const.DIGIT_0, byte]
            self.data(buf)

    def contrast(self, value):
        """
        Sets the LED intensity
        """
        assert(0 <= value <= 255)
        self.data([self._const.INTENSITY, value >> 4] * self.cascaded)

    def show(self):
        """
        Switches the display mode OFF, putting the device in low-power
        sleep mode.
        """
        self.data([self._const.SHUTDOWN, 1] * self.cascaded)

    def hide(self):
        """
        Sets the display mode ON, waking the device out of a prior
        low-power sleep mode.
        """
        self.data([self._const.SHUTDOWN, 0] * self.cascaded)
