# -*- coding: utf-8 -*-
# Copyright (c) 2017-19 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Collection of serial interfaces to LED matrix devices.
"""

# Example usage:
#
#   from luma.core.interface.serial import spi, noop
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

import luma.core.error
import luma.led_matrix.const
from luma.core.interface.serial import noop
from luma.core.device import device
from luma.core.render import canvas
from luma.core.util import observable
from luma.core.virtual import sevensegment
from luma.led_matrix.segment_mapper import dot_muncher, regular


__all__ = ["max7219", "ws2812", "neopixel", "neosegment", "apa102", "unicornhathd"]


class max7219(device):
    """
    Serial interface to a series of 8x8 LED matrixes daisychained together with
    MAX7219 chips.

    On creation, an initialization sequence is pumped to the display to properly
    configure it. Further control commands can then be called to affect the
    brightness and other settings.
    """
    def __init__(self, serial_interface=None, width=8, height=8, cascaded=None, rotate=0,
                 block_orientation=0, blocks_arranged_in_reverse_order=False, contrast=0x70,
                 **kwargs):
        super(max7219, self).__init__(luma.led_matrix.const.max7219, serial_interface)

        # Derive (override) the width and height if a cascaded param supplied
        if cascaded is not None:
            width = cascaded * 8
            height = 8

        self.blocks_arranged_in_reverse_order = blocks_arranged_in_reverse_order
        self.capabilities(width, height, rotate)
        self.segment_mapper = dot_muncher

        if width <= 0 or width % 8 != 0 or height <= 0 or height % 8 != 0:
            raise luma.core.error.DeviceDisplayModeError(
                "Unsupported display mode: {0} x {1}".format(width, height))

        assert block_orientation in [0, 90, -90, 180]
        self._correction_angle = block_orientation

        self.cascaded = cascaded or (width * height) // 64
        self._offsets = [(y * self._w) + x
                         for y in range(self._h - 8, -8, -8)
                         for x in range(self._w - 8, -8, -8)]
        self._rows = list(range(8))

        self.data([self._const.SCANLIMIT, 7] * self.cascaded)
        self.data([self._const.DECODEMODE, 0] * self.cascaded)
        self.data([self._const.DISPLAYTEST, 0] * self.cascaded)

        self.contrast(contrast)
        self.clear()
        self.show()

    def preprocess(self, image):
        """
        Performs the inherited behviour (if any), and if the LED matrix
        orientation is declared to need correction, each 8x8 block of pixels
        is rotated 90° clockwise or counter-clockwise.
        """
        image = super(max7219, self).preprocess(image)

        if self._correction_angle != 0:
            image = image.copy()
            for y in range(0, self._h, 8):
                for x in range(0, self._w, 8):
                    box = (x, y, x + 8, y + 8)
                    rotated_block = image.crop(box).rotate(self._correction_angle)
                    image.paste(rotated_block, box)
        if self.blocks_arranged_in_reverse_order:
            old_image = image.copy()
            for y in range(8):
                for x in range(8):
                    for i in range(self.cascaded):
                        image.putpixel((8 * (self.cascaded - 1) - i * 8 + x, y), old_image.getpixel((i * 8 + x, y)))

        return image

    def display(self, image):
        """
        Takes a 1-bit :py:mod:`PIL.Image` and dumps it to the LED matrix display
        via the MAX7219 serializers.
        """
        assert(image.mode == self.mode)
        assert(image.size == self.size)

        image = self.preprocess(image)

        i = 0
        d0 = self._const.DIGIT_0
        step = 2 * self.cascaded
        offsets = self._offsets
        rows = self._rows

        buf = bytearray(8 * step)
        pix = list(image.getdata())

        for digit in range(8):
            for daisychained_device in offsets:
                byte = 0
                idx = daisychained_device + digit
                for y in rows:
                    if pix[idx] > 0:
                        byte |= 1 << y
                    idx += self._w

                buf[i] = digit + d0
                buf[i + 1] = byte
                i += 2

        buf = list(buf)
        for i in range(0, len(buf), step):
            self.data(buf[i:i + step])

    def contrast(self, value):
        """
        Sets the LED intensity to the desired level, in the range 0-255.

        :param level: Desired contrast level in the range of 0-255.
        :type level: int
        """
        assert(0x00 <= value <= 0xFF)
        self.data([self._const.INTENSITY, value >> 4] * self.cascaded)

    def show(self):
        """
        Sets the display mode ON, waking the device out of a prior
        low-power sleep mode.
        """
        self.data([self._const.SHUTDOWN, 1] * self.cascaded)

    def hide(self):
        """
        Switches the display mode OFF, putting the device in low-power
        sleep mode.
        """
        self.data([self._const.SHUTDOWN, 0] * self.cascaded)


class ws2812(device):
    """
    Serial interface to a series of RGB neopixels daisy-chained together with
    WS281x chips.

    On creation, the array is initialized with the correct number of cascaded
    devices. Further control commands can then be called to affect the
    brightness and other settings.

    :param dma_interface: The WS2812 interface to write to (usually omit this
        parameter and it will default to the correct value - it is only needed
        for testing whereby a mock implementation is supplied).
    :param width: The number of pixels laid out horizontally.
    :type width: int
    :param height: The number of pixels laid out vertically.
    :type width: int
    :param cascaded: The number of pixels in a single strip - if supplied, this
        will override ``width`` and ``height``.
    :type cascaded: int
    :param rotate: Whether the device dimenstions should be rotated in-situ:
        A value of: 0=0°, 1=90°, 2=180°, 3=270°. If not supplied, zero is
        assumed.
    :type rotate: int
    :param mapping: An (optional) array of integer values that translate the
        pixel to physical offsets. If supplied, should be the same size as
        ``width * height``.
    :type mapping: int[]

    .. versionadded:: 0.4.0
    """
    def __init__(self, dma_interface=None, width=8, height=4, cascaded=None,
                 rotate=0, mapping=None, **kwargs):
        super(ws2812, self).__init__(const=None, serial_interface=noop)

        # Derive (override) the width and height if a cascaded param supplied
        if cascaded is not None:
            width = cascaded
            height = 1

        self.cascaded = width * height
        self.capabilities(width, height, rotate, mode="RGB")
        self._mapping = list(mapping or range(self.cascaded))
        assert(self.cascaded == len(self._mapping))
        self._contrast = None
        self._prev_contrast = 0x70

        ws = self._ws = dma_interface or self.__ws281x__()

        # Create ws2811_t structure and fill in parameters.
        self._leds = ws.new_ws2811_t()

        pin = 18
        channel = 0
        dma = 10
        freq_hz = 800000
        brightness = 255
        strip_type = ws.WS2811_STRIP_GRB
        invert = False

        # Initialize the channels to zero
        for channum in range(2):
            chan = ws.ws2811_channel_get(self._leds, channum)
            ws.ws2811_channel_t_count_set(chan, 0)
            ws.ws2811_channel_t_gpionum_set(chan, 0)
            ws.ws2811_channel_t_invert_set(chan, 0)
            ws.ws2811_channel_t_brightness_set(chan, 0)

        # Initialize the channel in use
        self._channel = ws.ws2811_channel_get(self._leds, channel)
        ws.ws2811_channel_t_count_set(self._channel, self.cascaded)
        ws.ws2811_channel_t_gpionum_set(self._channel, pin)
        ws.ws2811_channel_t_invert_set(self._channel, 0 if not invert else 1)
        ws.ws2811_channel_t_brightness_set(self._channel, brightness)
        ws.ws2811_channel_t_strip_type_set(self._channel, strip_type)

        # Initialize the controller
        ws.ws2811_t_freq_set(self._leds, freq_hz)
        ws.ws2811_t_dmanum_set(self._leds, dma)

        resp = ws.ws2811_init(self._leds)
        if resp != 0:
            raise RuntimeError('ws2811_init failed with code {0}'.format(resp))

        self.clear()
        self.show()

    def __ws281x__(self):
        import _rpi_ws281x
        return _rpi_ws281x

    def display(self, image):
        """
        Takes a 24-bit RGB :py:mod:`PIL.Image` and dumps it to the daisy-chained
        WS2812 neopixels.
        """
        assert(image.mode == self.mode)
        assert(image.size == self.size)

        ws = self._ws
        m = self._mapping
        for idx, (red, green, blue) in enumerate(image.getdata()):
            color = (red << 16) | (green << 8) | blue
            ws.ws2811_led_set(self._channel, m[idx], color)

        self._flush()

    def show(self):
        """
        Simulates switching the display mode ON; this is achieved by restoring
        the contrast to the level prior to the last time hide() was called.
        """
        if self._prev_contrast is not None:
            self.contrast(self._prev_contrast)
            self._prev_contrast = None

    def hide(self):
        """
        Simulates switching the display mode OFF; this is achieved by setting
        the contrast level to zero.
        """
        if self._prev_contrast is None:
            self._prev_contrast = self._contrast
            self.contrast(0x00)

    def contrast(self, value):
        """
        Sets the LED intensity to the desired level, in the range 0-255.

        :param level: Desired contrast level in the range of 0-255.
        :type level: int
        """
        assert(0x00 <= value <= 0xFF)
        self._contrast = value
        self._ws.ws2811_channel_t_brightness_set(self._channel, value)
        self._flush()

    def _flush(self):
        resp = self._ws.ws2811_render(self._leds)
        if resp != 0:
            raise RuntimeError('ws2811_render failed with code {0}'.format(resp))

    def __del__(self):
        # Required because Python will complain about memory leaks
        # However there's no guarantee that "ws" will even be set
        # when the __del__ method for this class is reached.
        if self._ws is not None:
            self.cleanup()

    def cleanup(self):
        """
        Attempt to reset the device & switching it off prior to exiting the
        python process.
        """
        self.hide()
        self.clear()

        if self._leds is not None:
            self._ws.ws2811_fini(self._leds)
            self._ws.delete_ws2811_t(self._leds)
            self._leds = None
            self._channel = None


# Alias for ws2812
neopixel = ws2812

# 8x8 Unicorn HAT has a 'snake-like' layout, so this translation
# mapper linearizes that arrangement into a 'scan-like' layout.
UNICORN_HAT = [
    7,  6,  5,  4,  3,  2,  1,  0,
    8,  9,  10, 11, 12, 13, 14, 15,
    23, 22, 21, 20, 19, 18, 17, 16,
    24, 25, 26, 27, 28, 29, 30, 31,
    39, 38, 37, 36, 35, 34, 33, 32,
    40, 41, 42, 43, 44, 45, 46, 47,
    55, 54, 53, 52, 51, 50, 49, 48,
    56, 57, 58, 59, 60, 61, 62, 63
]


class apa102(device):
    """
    Serial interface to a series of 'next-gen' RGB neopixels daisy-chained
    together with APA102 chips.

    On creation, the array is initialized with the correct number of cascaded
    devices. Further control commands can then be called to affect the brightness
    and other settings.

    Note that the brightness of individual pixels can be set by altering the
    alpha channel of the RGBA image that is being displayed.

    :param serial_interface: The serial interface to write to (usually omit this
        parameter and it will default to the correct value - it is only needed
        for testing whereby a mock implementation is supplied).
    :param width: The number of pixels laid out horizontally.
    :type width: int
    :param height: The number of pixels laid out vertically.
    :type width: int
    :param cascaded: The number of pixels in a single strip - if supplied, this
        will override ``width`` and ``height``.
    :type cascaded: int
    :param rotate: Whether the device dimenstions should be rotated in-situ:
        A value of: 0=0°, 1=90°, 2=180°, 3=270°. If not supplied, zero is
        assumed.
    :type rotate: int
    :param mapping: An (optional) array of integer values that translate the
        pixel to physical offsets. If supplied, should be the same size as
        ``width * height``.
    :type mapping: int[]

    .. versionadded:: 0.9.0
    """
    def __init__(self, serial_interface=None, width=8, height=1, cascaded=None,
                 rotate=0, mapping=None, **kwargs):
        super(apa102, self).__init__(luma.core.const.common, serial_interface or self.__bitbang__())

        # Derive (override) the width and height if a cascaded param supplied
        if cascaded is not None:
            width = cascaded
            height = 1

        self.cascaded = width * height
        self.capabilities(width, height, rotate, mode="RGBA")
        self._mapping = list(mapping or range(self.cascaded))
        assert(self.cascaded == len(self._mapping))
        self._last_image = None

        self.contrast(0x70)
        self.clear()
        self.show()

    def __bitbang__(self):
        from luma.core.interface.serial import bitbang
        return bitbang(SCLK=24, SDA=23)

    def display(self, image):
        """
        Takes a 32-bit RGBA :py:mod:`PIL.Image` and dumps it to the daisy-chained
        APA102 neopixels. If a pixel is not fully opaque, the alpha channel
        value is used to set the brightness of the respective RGB LED.
        """
        assert(image.mode == self.mode)
        assert(image.size == self.size)
        self._last_image = image.copy()

        # Send zeros to reset, then pixel values then zeros at end
        sz = image.width * image.height * 4
        buf = bytearray(sz * 3)

        m = self._mapping
        for idx, (r, g, b, a) in enumerate(image.getdata()):
            offset = sz + m[idx] * 4
            brightness = (a >> 4) if a != 0xFF else self._brightness
            buf[offset] = (0xE0 | brightness)
            buf[offset + 1] = b
            buf[offset + 2] = g
            buf[offset + 3] = r

        self._serial_interface.data(list(buf))

    def show(self):
        """
        Not supported
        """
        pass

    def hide(self):
        """
        Not supported
        """
        pass

    def contrast(self, value):
        """
        Sets the LED intensity to the desired level, in the range 0-255.

        :param level: Desired contrast level in the range of 0-255.
        :type level: int
        """
        assert(0x00 <= value <= 0xFF)
        self._brightness = value >> 4
        if self._last_image is not None:
            self.display(self._last_image)


class neosegment(sevensegment):
    """
    Extends the :py:class:`~luma.core.virtual.sevensegment` class specifically
    for @msurguy's modular NeoSegments. It uses the same underlying render
    techniques as the base class, but provides additional functionality to be
    able to adddress individual characters colors.

    :param width: The number of 7-segment elements that are cascaded.
    :type width: int
    :param undefined: The default character to substitute when an unrenderable
        character is supplied to the text property.
    :type undefined: char

    .. versionadded:: 0.11.0
    """
    def __init__(self, width, undefined="_", **kwargs):
        if width <= 0 or width % 2 == 1:
            raise luma.core.error.DeviceDisplayModeError(
                "Unsupported display mode: width={0}".format(width))

        height = 7
        mapping = [(i % width) * height + (i // width) for i in range(width * height)]
        self.device = kwargs.get("device") or ws2812(width=width, height=height, mapping=mapping)
        self.undefined = undefined
        self._text_buffer = ""
        self.color = "white"

    @property
    def color(self):
        return self._colors

    @color.setter
    def color(self, value):
        if not isinstance(value, list):
            value = [value] * self.device.width

        assert(len(value) == self.device.width)
        self._colors = observable(value, observer=self._color_chg)

    def _color_chg(self, color):
        self._flush(self.text, color)

    def _flush(self, text, color=None):
        data = bytearray(self.segment_mapper(text, notfound=self.undefined)).ljust(self.device.width, b'\0')
        color = color or self.color

        if len(data) > self.device.width:
            raise OverflowError(
                "Device's capabilities insufficient for value '{0}'".format(text))

        with canvas(self.device) as draw:
            for x, byte in enumerate(data):
                for y in range(self.device.height):
                    if byte & 0x01:
                        draw.point((x, y), fill=color[x])
                    byte >>= 1

    def segment_mapper(self, text, notfound="_"):
        for char in regular(text, notfound):

            # Convert from std MAX7219 segment mappings
            a = char >> 6 & 0x01
            b = char >> 5 & 0x01
            c = char >> 4 & 0x01
            d = char >> 3 & 0x01
            e = char >> 2 & 0x01
            f = char >> 1 & 0x01
            g = char >> 0 & 0x01

            # To NeoSegment positions
            yield \
                b << 6 | \
                a << 5 | \
                f << 4 | \
                g << 3 | \
                c << 2 | \
                d << 1 | \
                e << 0


class unicornhathd(device):
    """
    Display adapter for Pimoroni's Unicorn Hat HD - a dense 16x16 array of
    high intensity RGB LEDs. Since the board contains a small ARM chip to
    manage the LEDs, interfacing is very straightforward using SPI. This has
    the side-effect that the board appears not to be daisy-chainable though.
    However there a number of undocumented contact pads on the underside of
    the board which _may_ allow this behaviour.

    Note that the brightness of individual pixels can be set by altering the
    alpha channel of the RGBA image that is being displayed.

    :param serial_interface: The serial interface to write to.
    :param rotate: Whether the device dimenstions should be rotated in-situ:
        A value of: 0=0°, 1=90°, 2=180°, 3=270°. If not supplied, zero is
        assumed.
    :type rotate: int

    .. versionadded:: 1.3.0
    """
    def __init__(self, serial_interface=None, rotate=0, **kwargs):
        super(unicornhathd, self).__init__(luma.core.const.common, serial_interface)
        self.capabilities(16, 16, rotate, mode="RGBA")
        self._last_image = None
        self._prev_brightness = None
        self.contrast(0x70)
        self.clear()
        self.show()

    def display(self, image):
        """
        Takes a 32-bit RGBA :py:mod:`PIL.Image` and dumps it to the Unicorn HAT HD.
        If a pixel is not fully opaque, the alpha channel value is used to set the
        brightness of the respective RGB LED.
        """
        assert(image.mode == self.mode)
        assert(image.size == self.size)
        self._last_image = image.copy()

        # Send zeros to reset, then pixel values then zeros at end
        sz = image.width * image.height * 3
        buf = bytearray(sz)
        normalized_brightness = self._brightness / 255.0

        for idx, (r, g, b, a) in enumerate(image.getdata()):
            offset = idx * 3
            brightness = a / 255.0 if a != 255 else normalized_brightness
            buf[offset] = int(r * brightness)
            buf[offset + 1] = int(g * brightness)
            buf[offset + 2] = int(b * brightness)

        self._serial_interface.data([0x72] + list(buf))   # 0x72 == SOF ... start of frame?

    def show(self):
        """
        Simulates switching the display mode ON; this is achieved by restoring
        the contrast to the level prior to the last time hide() was called.
        """
        if self._prev_brightness is not None:
            self.contrast(self._prev_brightness)
            self._prev_brightness = None

    def hide(self):
        """
        Simulates switching the display mode OFF; this is achieved by setting
        the contrast level to zero.
        """
        if self._prev_brightness is None:
            self._prev_brightness = self._brightness
            self.contrast(0x00)

    def contrast(self, value):
        """
        Sets the LED intensity to the desired level, in the range 0-255.

        :param level: Desired contrast level in the range of 0-255.
        :type level: int
        """
        assert(0x00 <= value <= 0xFF)
        self._brightness = value
        if self._last_image is not None:
            self.display(self._last_image)
