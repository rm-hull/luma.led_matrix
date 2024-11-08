#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.

from math import ceil
from luma.led_matrix.device import apa102
from luma.core.render import canvas

from helpers import serial, setup_function  # noqa: F401


def start_frame():
    return [0] * 4


def end_frame(n):
    return [0] * ceil(n / 2 / 8)


def test_init_cascaded():
    device = apa102(serial, cascaded=7)
    assert device.width == 7
    assert device.height == 1
    serial.data.assert_called_with(start_frame() + [0xE0, 0, 0, 0] * 7 + end_frame(7))


def test_hide():
    device = apa102(serial, cascaded=5)
    serial.reset_mock()
    device.hide()
    serial.data.assert_not_called()


def test_show():
    device = apa102(serial, cascaded=5)
    serial.reset_mock()
    device.show()
    serial.data.assert_not_called()


def test_contrast():
    device = apa102(serial, cascaded=6)
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="red")
    serial.reset_mock()
    device.contrast(0x6B)
    serial.data.assert_called_with(
        start_frame() + [0xE6, 0, 0, 0xFF] * 6 + end_frame(6)
    )


def test_display():
    device = apa102(serial, width=4, height=1)
    serial.reset_mock()

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline=(0x11, 0x22, 0x33, 0x44))

    serial.data.assert_called_with(
        start_frame() + [0xE4, 0x33, 0x22, 0x11] * 4 + end_frame(4)
    )
