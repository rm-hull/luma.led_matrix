# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.

# Example usage:
#
#   from luma.core.serial import spi
#   from luma.core.render import canvas
#   from luma.led_matrix.device import max7219
#
#   serial = spi(port=0, device=0)
#   device = max7219(serial, width=8, height=8)
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
from luma.core.render import canvas
import luma.core.error
import luma.led_matrix.const
from luma.led_matrix.segment_mapper import dot_muncher
from luma.led_matrix.helpers import mutable_string, observable


class max7219(device):
    """
    Encapsulates the serial interface to a series of 8x8 LED matrixes
    daisychained together with MAX7219 chips. On creation, an initialization
    sequence is pumped to the display to properly configure it. Further control
    commands can then be called to affect the brightness and other settings.
    """
    def __init__(self, serial_interface=None, width=8, height=8, cascaded=None, rotate=0):
        super(max7219, self).__init__(luma.led_matrix.const.max7219, serial_interface)

        # Derive (override) the width and height if a cascaded param supplied
        if cascaded is not None:
            width = cascaded * 8
            height = 8

        self.capabilities(width, height, rotate)

        # Currently only allow a strip of matrices
        # TODO: Future enhancement - allow blocks, e.g 40x16 (5x2 blocks)
        if width % 8 != 0 or height != 8:
            raise luma.core.error.DeviceDisplayModeError(
                "Unsupported display mode: {0} x {1}".format(width, height))

        self.cascaded = cascaded or width // 8

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
            for daisychained_device in reversed(list(range(self.cascaded))):
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


class sevensegment(object):
    """
    Abstraction that wraps a MAX7219 device, this class provides a ``text``
    property which can be used to set and get a value, which is propagated
    onto the underlying device.

    :param device: A MAX7219 device instance
    :param undefined: The default character to substitute when an unrenderable
        character is supplied to the text property.
    :type undefined: char
    :param mapper: A function that maps strings into the correct
        representation for the 7-segment physical layout. By default, a "dot"
        muncher implementation is used which places dots inline with the
        preceeding character.
    """
    def __init__(self, device, undefined="_", mapper=dot_muncher):
        self.device = device
        self.undefined = undefined
        self.segment_mapper = mapper
        self._bufsize = device.width * device.height // 8
        self.text = ""

    @property
    def text(self):
        """
        Returns the current state of the text buffer. This may not reflect
        accurately what is displayed on the seven-segment device, as certain
        alpha-numerics and most punctuation cannot be rendered on the limited
        display
        """
        return self._text_buffer

    @text.setter
    def text(self, value):
        """
        Updates the seven-segment display with the given value. If there is not
        enough space to show the full text, an ``OverflowException`` is raised.
        """
        self._text_buffer = observable(mutable_string(value), observer=self._flush)

    def _flush(self, buf):
        data = bytearray(self.segment_mapper(buf, notfound=self.undefined)).ljust(self._bufsize, b'\0')

        if len(data) > self._bufsize:
            raise OverflowError("Device's capabilities insufficent for value '{0}'".format(buf))

        with canvas(self.device) as draw:
            for x, byte in enumerate(reversed(data)):
                for y in range(8):
                    if byte & 0x01:
                        draw.point((x, y), fill="white")
                    byte >>= 1
