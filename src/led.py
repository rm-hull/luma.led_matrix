#!/usr/bin/env python
# -*- coding: utf-8 -*-

import max7219.spi as spi
import time

from max7219.font import cp437_FONT

class constants(object):
    MAX7219_REG_NOOP        = 0x0
    MAX7219_REG_DIGIT0      = 0x1
    MAX7219_REG_DIGIT1      = 0x2
    MAX7219_REG_DIGIT2      = 0x3
    MAX7219_REG_DIGIT3      = 0x4
    MAX7219_REG_DIGIT4      = 0x5
    MAX7219_REG_DIGIT5      = 0x6
    MAX7219_REG_DIGIT6      = 0x7
    MAX7219_REG_DIGIT7      = 0x8
    MAX7219_REG_DECODEMODE  = 0x9
    MAX7219_REG_INTENSITY   = 0xA
    MAX7219_REG_SCANLIMIT   = 0xB
    MAX7219_REG_SHUTDOWN    = 0xC
    MAX7219_REG_DISPLAYTEST = 0xF

class device(object):
    """
    Base class for handling multiple cascaded MAX7219 devices.
    Callers should generally pick either the sevensegment or matrix
    subclasses instead depending on which application is required.

    A buffer is maintained which holds the bytes that will be cascaded
    every time flush() is called.
    """
    NUM_DIGITS = 8

    def __init__(self, cascaded=1):
        """
        Constructor: cascaded should be the number of cascaded MAX7219
        devices are connected.
        """
        assert cascaded > 0, "Must have at least one device!"
        self._cascaded = cascaded
        self._buffer = [0] * self.NUM_DIGITS * self._cascaded
        spi.openSPI(speed=1000000)

        self._write(
            constants.MAX7219_REG_SCANLIMIT, 7,   # show all 8 digits
            constants.MAX7219_REG_DECODEMODE, 0,  # using a LED matrix (not digits)
            constants.MAX7219_REG_DISPLAYTEST, 0, # no display test
            constants.MAX7219_REG_SHUTDOWN, 1)    # not in shutdown mode (i.e start it up)
        self.brightness(7)                        # character intensity: range: 0..15
        self.clear()

    def _write(self, *bytes):
        """
        Send the bytes (which should comprise of alternating command,
        data values) over the SPI device.
        """
        spi.transfer(bytes)

    def _values(self, position):
        """
        A generator which yields the digit/column position and the data
        value from that position for each of the cascaded devices.
        """
        for deviceId in xrange(self._cascaded):
            yield position + constants.MAX7219_REG_DIGIT0
            yield self._buffer[(deviceId * self.NUM_DIGITS) + position]

    def clear(self, deviceId=None):
        """
        Clears the buffer the given deviceId if specified (else clears all devices), and flushes.
        """
        assert not deviceId or 0 <= deviceId < self._cascaded, "Invalid deviceId: {0}".format(deviceId)

        if deviceId is None:
            start = 0
            end = self._cascaded
        else:
            start = deviceId
            end = deviceId + 1

        for deviceId in xrange(start, end):
            for position in xrange(self.NUM_DIGITS):
                self.set_byte(deviceId, position + constants.MAX7219_REG_DIGIT0, 0, redraw=False)

        self.flush()

    def flush(self):
        """
        For each digit/column, cascade out the contents of the buffer
        cells to the SPI device.
        """
        for posn in xrange(self.NUM_DIGITS):
            self._write(*tuple(self._values(posn)))

    def brightness(self, intensity):
        """
        Sets the brightness level of all cascaded devices to the same
        intensity level, ranging from 0..16
        """
        assert 0 <= intensity < 16, "Invalid brightness: {0}".format(intensity)
        for _ in xrange(self._cascaded):
            self._write(constants.MAX7219_REG_INTENSITY, intensity)

    def set_byte(self, deviceId, position, value, redraw=True):
        """
        Low level mechanism to set a byte value in the buffer array. If redraw
        is not suppled, or set to True, will force a redraw of _all_ buffer
        items: If you are calling this method rapidly/frequently (e.g in a
        loop), it would be more efficient to set to False, and when done,
        call flush().

        Prefer to use the higher-level method calls in the subclasses below.
        """
        assert 0 <= deviceId < self._cascaded, "Invalid deviceId: {0}".format(deviceId)
        assert constants.MAX7219_REG_DIGIT0 <= position <= constants.MAX7219_REG_DIGIT7, "Invalid digit/column: {0}".format(position)

        offset = (deviceId * self.NUM_DIGITS) + position - constants.MAX7219_REG_DIGIT0
        self._buffer[offset] = value

        if redraw:
            self.flush()

class sevensegment(device):
    """
    Implementation of MAX7219 devices cascaded with a series of seven-segment
    LEDs. It provides a convenient method to write a number to a given device
    in octal, decimal or hex, flushed left/right with zero padding. Base 10
    numbers can be either integers or floating point (with the number of
    decimal points configurable).
    """
    radix = {8: 'o', 10: 'f', 16: 'x'}
    digits = {
        ' ': 0x00,
        '-': 0x01,
        '0': 0x7e,
        '1': 0x30,
        '2': 0x6d,
        '3': 0x79,
        '4': 0x33,
        '5': 0x5b,
        '6': 0x5f,
        '7': 0x70,
        '8': 0x7f,
        '9': 0x7b,
        'a': 0x77,
        'b': 0x1f,
        'c': 0x4e,
        'd': 0x3d,
        'e': 0x4f,
        'f': 0x47
    }

    def write_number(self, deviceId, value, base=10, decimalPlaces=0, zeroPad=False, leftJustify=False):
        """
        Formats the value according to the parameters supplied, and displays
        on the specified device. If the formatted number is larger than
        8 digits, then an OverflowError is raised.
        """
        assert 0 <= deviceId < self._cascaded, "Invalid deviceId: {0}".format(deviceId)
        assert base in self.radix, "Invalid base: {0}".format(base)

        # Magic up a printf format string
        size = self.NUM_DIGITS
        formatStr = '%'
        if zeroPad: formatStr += '0'
        if decimalPlaces > 0: size += 1
        if leftJustify: size *= -1
        formatStr = '{fmt}{size}.{dp}{type}'.format(
                        fmt=formatStr, size=size, dp=decimalPlaces, type=self.radix[base])

        position = constants.MAX7219_REG_DIGIT7
        strValue = formatStr % value

        # Go through each digit in the formatted string,
        # updating the buffer accordingly
        for char in strValue:

            if position < constants.MAX7219_REG_DIGIT0:
                self.clear(deviceId)
                raise OverflowError('{0} too large for display'.format(strValue));

            if char == '.':
                continue

            dp = (decimalPlaces > 0 and position == decimalPlaces + 1)
            value = self.digits[char] | (dp << 7)
            self.set_byte(deviceId, position, value, redraw=False)
            position -= 1

        self.flush()


#class matrix(device):
#
#    def letter(self, char, font=cp437_FONT):
#        for col in range(self.NUM_DIGITS):
#            send_byte(col + 1, font[char][col])#
#
#    def show_message(self, text, transition, font=cp437_FONT):
#        prev = ' '
#        for curr in text:
#            transition(ord(prev), ord(curr), font)
#            prev = curr
#        transition(ord(prev), 32)

