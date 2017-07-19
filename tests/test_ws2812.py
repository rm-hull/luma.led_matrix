#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.

from luma.led_matrix.device import neopixel
from luma.core.render import canvas

from helpers import Mock, call


ws2812 = Mock(unsafe=True)


def setup_function(function):
    ws2812.reset_mock()
    ws2812.command.side_effect = None


def test_init_cascaded():
    device = neopixel(ws2812, cascaded=7)
    assert device.width == 7
    assert device.height == 1
    ws2812.init.assert_called_once_with(7)
    ws2812.setPixelColorRGB.assert_has_calls([
        call(i, 0, 0, 0) for i in range(7)])


def test_init_4x8():
    device = neopixel(ws2812)
    assert device.cascaded == 32
    ws2812.init.assert_called_once_with(32)
    ws2812.setPixelColorRGB.assert_has_calls([
        call(i, 0, 0, 0) for i in range(32)])


def test_hide():
    device = neopixel(ws2812, cascaded=5)
    ws2812.reset_mock()
    device.hide()
    ws2812.setPixelColorRGB.assert_not_called()
    ws2812.show.assert_not_called()


def test_show():
    device = neopixel(ws2812, cascaded=5)
    ws2812.reset_mock()
    device.show()
    ws2812.setPixelColorRGB.assert_not_called()
    ws2812.show.assert_not_called()


def test_contrast():
    device = neopixel(ws2812, cascaded=6)
    ws2812.reset_mock()
    device.contrast(0x6B)
    ws2812.setBrightness.assert_called_once_with(0.4196078431372549)


def test_display():
    device = neopixel(ws2812, width=4, height=4)
    ws2812.reset_mock()

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="red")

    ws2812.setPixelColorRGB.assert_has_calls([
        call(0, 0xFF, 0, 0),
        call(1, 0xFF, 0, 0),
        call(2, 0xFF, 0, 0),
        call(3, 0xFF, 0, 0),
        call(4, 0xFF, 0, 0),
        call(5, 0, 0, 0),
        call(6, 0, 0, 0),
        call(7, 0xFF, 0, 0),
        call(8, 0xFF, 0, 0),
        call(9, 0, 0, 0),
        call(10, 0, 0, 0),
        call(11, 0xFF, 0, 0),
        call(12, 0xFF, 0, 0),
        call(13, 0xFF, 0, 0),
        call(14, 0xFF, 0, 0),
        call(15, 0xFF, 0, 0),
    ])
    assert ws2812.show.called


def test_mapping():
    num_pixels = 16
    device = neopixel(ws2812, cascaded=num_pixels, mapping=reversed(list(range(num_pixels))))
    ws2812.reset_mock()

    with canvas(device) as draw:
        for i in range(device.cascaded):
            draw.point((i, 0), (i, 0, 0))

    expected = [call(num_pixels - i - 1, i, 0, 0) for i in range(num_pixels)]
    ws2812.setPixelColorRGB.assert_has_calls(expected)

    assert ws2812.show.called
