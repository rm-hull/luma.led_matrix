# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.

# Example usage:
#
#   from luma.core.serial import spi, noop
#   from luma.core.render import canvas
#   from luma.led_matrix.device import max7219
#
#   serial = spi(port=0, device=0, gpio=noop())
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

from luma.core.render import canvas
from luma.led_matrix.segment_mapper import dot_muncher
from luma.led_matrix.helpers import mutable_string, observable


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

        :param value: The value to render onto the device. Any characters which
            cannot be rendered will be converted into the ``undefined``
            character supplied in the constructor.
        :type value: string
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
