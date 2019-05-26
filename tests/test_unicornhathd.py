#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-19 Richard Hull and contributors
# See LICENSE.rst for details.

from luma.led_matrix.device import unicornhathd
from luma.core.render import canvas

from helpers import serial, call  # noqa: F401
from baseline_data import get_json_data


def test_init():
    device = unicornhathd(serial)
    assert device.width == 16
    assert device.height == 16
    serial.data.assert_called_once_with([0x72] + [0] * 256 * 3)


def test_hide():
    device = unicornhathd(serial)
    serial.reset_mock()
    device.hide()
    serial.data.assert_called_once_with([0x72] + [0] * 256 * 3)


def test_show():
    device = unicornhathd(serial)
    device.contrast(0xFF)
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="white")
    device.hide()
    serial.reset_mock()
    device.show()
    serial.data.assert_called_once_with([0x72] + [0xFF] * 256 * 3)


def test_contrast():
    device = unicornhathd(serial)
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="white")
    serial.reset_mock()
    device.contrast(0x6B)
    serial.data.assert_called_once_with([0x72] + [0x6B] * 256 * 3)


def test_display():
    device = unicornhathd(serial)
    serial.reset_mock()
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white")
    serial.data.assert_called_once_with([0x72] + get_json_data('demo_unicornhathd'))


def test_alpha_blending():
    device = unicornhathd(serial)
    serial.reset_mock()
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline=(255, 128, 64, 32))
    serial.data.assert_called_once_with([0x72] + get_json_data('demo_unicornhathd_alphablend'))
