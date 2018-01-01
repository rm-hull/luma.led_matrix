#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.

import pytest

from luma.led_matrix.device import neopixel
from luma.core.render import canvas

from helpers import Mock, call


ws = Mock(unsafe=True)
chan = "channel"
leds = "leds"


def setup_function(function):
    ws.reset_mock()
    ws.command.side_effect = None
    ws.ws2811_init = Mock(return_value=0)
    ws.ws2811_render = Mock(return_value=0)
    ws.ws2811_channel_get = Mock(return_value=chan)
    ws.ws2811_new_ws2811_t = Mock(return_value=leds)


def test_init_cascaded():
    device = neopixel(ws, cascaded=7)
    assert device.width == 7
    assert device.height == 1
    assert ws.ws2811_channel_t_count_set.called
    assert ws.ws2811_channel_t_gpionum_set.called
    assert ws.ws2811_channel_t_invert_set.called
    assert ws.ws2811_channel_t_brightness_set.called
    assert ws.ws2811_channel_t_strip_type_set.called
    assert ws.ws2811_t_freq_set.called
    assert ws.ws2811_t_dmanum_set.called
    assert ws.ws2811_init.called
    ws.ws2811_led_set.assert_has_calls([
        call(chan, i, 0x000000) for i in range(7)])
    assert ws.ws2811_render.called


def test_init_4x8():
    device = neopixel(ws)
    assert device.cascaded == 32
    assert ws.ws2811_channel_t_count_set.called
    assert ws.ws2811_channel_t_gpionum_set.called
    assert ws.ws2811_channel_t_invert_set.called
    assert ws.ws2811_channel_t_brightness_set.called
    assert ws.ws2811_channel_t_strip_type_set.called
    assert ws.ws2811_t_freq_set.called
    assert ws.ws2811_t_dmanum_set.called
    assert ws.ws2811_init.called
    ws.ws2811_led_set.assert_has_calls([
        call(chan, i, 0x000000) for i in range(32)])
    assert ws.ws2811_render.called


def test_init_fail():
    ws.reset_mock()
    ws.ws2811_init = Mock(return_value=-1)
    with pytest.raises(RuntimeError) as ex:
        neopixel(ws, cascaded=7)
    assert "ws2811_init failed with code -1" in str(ex.value)


def test_clear():
    device = neopixel(ws)
    ws.reset_mock()
    device.clear()
    ws.ws2811_led_set.assert_has_calls([
        call(chan, i, 0x000000) for i in range(32)])
    assert ws.ws2811_render.called


def test_cleanup():
    device = neopixel(ws)
    device.cleanup()
    ws.ws2811_led_set.assert_has_calls([
        call(chan, i, 0x000000) for i in range(32)])
    assert ws.ws2811_render.called
    assert ws.ws2811_fini.called
    assert ws.delete_ws2811_t.called
    assert device._leds is None
    assert device._channel is None


def test_hide():
    device = neopixel(ws, cascaded=5)
    ws.reset_mock()
    device.hide()
    ws.ws2811_led_set.assert_not_called()
    assert ws.ws2811_render.called


def test_show():
    device = neopixel(ws, cascaded=5)
    ws.reset_mock()
    device.hide()
    device.show()
    ws.ws2811_led_set.assert_not_called()
    assert ws.ws2811_render.called


def test_contrast():
    device = neopixel(ws, cascaded=6)
    ws.reset_mock()
    device.contrast(0x6B)
    ws.ws2811_channel_t_brightness_set.assert_called_once_with(chan, 0x6B)


def test_display():
    device = neopixel(ws, width=4, height=4)
    ws.reset_mock()

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="red")

    ws.ws2811_led_set.assert_has_calls([
        call(chan, 0, 0xFF0000),
        call(chan, 1, 0xFF0000),
        call(chan, 2, 0xFF0000),
        call(chan, 3, 0xFF0000),
        call(chan, 4, 0xFF0000),
        call(chan, 5, 0x000000),
        call(chan, 6, 0x000000),
        call(chan, 7, 0xFF0000),
        call(chan, 8, 0xFF0000),
        call(chan, 9, 0x000000),
        call(chan, 10, 0x000000),
        call(chan, 11, 0xFF0000),
        call(chan, 12, 0xFF0000),
        call(chan, 13, 0xFF0000),
        call(chan, 14, 0xFF0000),
        call(chan, 15, 0xFF0000),
    ])
    assert ws.ws2811_render.called


def test_display_fail():
    device = neopixel(ws, cascaded=7)
    ws.reset_mock()
    ws.ws2811_render = Mock(return_value=-1)

    with pytest.raises(RuntimeError) as ex:
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="red")

    assert "ws2811_render failed with code -1" in str(ex.value)


def test_mapping():
    num_pixels = 16
    device = neopixel(ws, cascaded=num_pixels, mapping=reversed(list(range(num_pixels))))
    ws.reset_mock()

    with canvas(device) as draw:
        for i in range(device.cascaded):
            draw.point((i, 0), (i, 0, 0))

    expected = [call(chan, num_pixels - i - 1, i << 16) for i in range(num_pixels)]
    ws.ws2811_led_set.assert_has_calls(expected)

    assert ws.ws2811_render.called
