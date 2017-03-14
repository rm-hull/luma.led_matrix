#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.

import pytest

from luma.led_matrix.device import max7219
from luma.core.render import canvas

from helpers import setup_function, serial, call, assert_invalid_dimensions  # noqa: F401


def test_init_cascaded():
    device = max7219(serial, cascaded=4)
    assert device.width == 32
    assert device.height == 8


def test_init_8x8():
    device = max7219(serial)
    assert device.cascaded == 1
    serial.data.assert_has_calls([
        call([11, 7]),
        call([9, 0]),
        call([15, 0]),
        call([10, 7]),
        call([1, 0]),
        call([2, 0]),
        call([3, 0]),
        call([4, 0]),
        call([5, 0]),
        call([6, 0]),
        call([7, 0]),
        call([8, 0]),
        call([12, 1])
    ])


def test_init_16x8():
    device = max7219(serial, width=16, height=8)
    assert device.cascaded == 2
    serial.data.assert_has_calls([
        call([11, 7, 11, 7]),
        call([9, 0, 9, 0]),
        call([15, 0, 15, 0]),
        call([10, 7, 10, 7]),
        call([1, 0, 1, 0]),
        call([2, 0, 2, 0]),
        call([3, 0, 3, 0]),
        call([4, 0, 4, 0]),
        call([5, 0, 5, 0]),
        call([6, 0, 6, 0]),
        call([7, 0, 7, 0]),
        call([8, 0, 8, 0]),
        call([12, 1, 12, 1])
    ])


def test_init_invalid_dimensions():
    assert_invalid_dimensions(max7219, serial, 59, 22)


def test_hide():
    device = max7219(serial, cascaded=5)
    serial.reset_mock()
    device.hide()
    serial.data.assert_called_once_with([12, 0] * 5)


def test_show():
    device = max7219(serial, cascaded=3)
    serial.reset_mock()
    device.show()
    serial.data.assert_called_once_with([12, 1] * 3)


def test_contrast():
    device = max7219(serial, cascaded=6)
    serial.reset_mock()
    device.contrast(0x6B)
    serial.data.assert_called_once_with([10, 6] * 6)


def test_display_16x8():
    device = max7219(serial, cascaded=2)
    serial.reset_mock()

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white")

    serial.data.assert_has_calls([
        call([1, 0x81, 1, 0xFF]),
        call([2, 0x81, 2, 0x81]),
        call([3, 0x81, 3, 0x81]),
        call([4, 0x81, 4, 0x81]),
        call([5, 0x81, 5, 0x81]),
        call([6, 0x81, 6, 0x81]),
        call([7, 0x81, 7, 0x81]),
        call([8, 0xFF, 8, 0x81])
    ])


def test_display_16x16():
    device = max7219(serial, width=16, height=16)
    serial.reset_mock()

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white")

    serial.data.assert_has_calls([
        call([1, 0x80, 1, 0xFF, 1, 0x01, 1, 0xFF]),
        call([2, 0x80, 2, 0x80, 2, 0x01, 2, 0x01]),
        call([3, 0x80, 3, 0x80, 3, 0x01, 3, 0x01]),
        call([4, 0x80, 4, 0x80, 4, 0x01, 4, 0x01]),
        call([5, 0x80, 5, 0x80, 5, 0x01, 5, 0x01]),
        call([6, 0x80, 6, 0x80, 6, 0x01, 6, 0x01]),
        call([7, 0x80, 7, 0x80, 7, 0x01, 7, 0x01]),
        call([8, 0xFF, 8, 0x80, 8, 0xFF, 8, 0x01])
    ])


def test_normal_alignment():
    device = max7219(serial, cascaded=2, block_orientation="horizontal")
    serial.reset_mock()

    with canvas(device) as draw:
        draw.rectangle((0, 0, 15, 3), outline="white")

    serial.data.assert_has_calls([
        call([1, 0x09, 1, 0x0F]),
        call([2, 0x09, 2, 0x09]),
        call([3, 0x09, 3, 0x09]),
        call([4, 0x09, 4, 0x09]),
        call([5, 0x09, 5, 0x09]),
        call([6, 0x09, 6, 0x09]),
        call([7, 0x09, 7, 0x09]),
        call([8, 0x0F, 8, 0x09])
    ])


def test_block_realignment():
    device = max7219(serial, cascaded=2, block_orientation="vertical")
    serial.reset_mock()

    with canvas(device) as draw:
        draw.rectangle((0, 0, 15, 3), outline="white")

    serial.data.assert_has_calls([
        call([1, 0x00, 1, 0x00]),
        call([2, 0x00, 2, 0x00]),
        call([3, 0x00, 3, 0x00]),
        call([4, 0x00, 4, 0x00]),
        call([5, 0xFF, 5, 0xFF]),
        call([6, 0x80, 6, 0x01]),
        call([7, 0x80, 7, 0x01]),
        call([8, 0xFF, 8, 0xFF])
    ])


def test_unknown_block_orientation():
    with pytest.raises(AssertionError):
        max7219(serial, cascaded=2, block_orientation="sausages")
