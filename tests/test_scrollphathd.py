#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2026 Richard Hull and contributors
# See LICENSE.rst for details.

from unittest.mock import Mock, call

import pytest

from luma.led_matrix.device import scrollphathd
from luma.led_matrix.const import is31fl3731
from luma.core.render import canvas


NUM_PIXELS = is31fl3731.NUM_PIXELS


@pytest.fixture
def i2c_bus():
    return Mock(unsafe=True)


# The full 17x7 -> 144-pixel address mapping, and the corresponding LED
# "wired up" enable bitmap, cross-checked against Pimoroni's published
# scrollphathd enable pattern for the same board.
ENABLE_BITMAP = [
    0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111,
    0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111,
    0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b01111111, 0b00000000,
]


def blank_pwm():
    return [0] * NUM_PIXELS


def test_init_default_address(i2c_bus):
    scrollphathd(i2c_bus)
    i2c_bus.write_byte_data.assert_any_call(0x74, 0xFD, 0x0B)


def test_init_custom_address(i2c_bus):
    scrollphathd(i2c_bus, address=0x77)
    i2c_bus.write_byte_data.assert_any_call(0x77, 0xFD, 0x0B)


def test_init_dimensions(i2c_bus):
    device = scrollphathd(i2c_bus)
    assert device.width == 17
    assert device.height == 7


def test_init_enables_only_wired_leds(i2c_bus):
    scrollphathd(i2c_bus)

    # Bank select for frame 0 followed by the enable bitmap write; since
    # all 8 frames get identically configured, just check the first.
    i2c_bus.write_i2c_block_data.assert_any_call(0x74, 0x00, ENABLE_BITMAP)


def test_init_clears_and_wakes(i2c_bus):
    scrollphathd(i2c_bus)

    # A blank frame should have been written out (all zero PWM values)...
    i2c_bus.write_i2c_block_data.assert_any_call(0x74, 0x24, blank_pwm()[0:32])

    # ...and the device should have been woken (shutdown register cleared
    # low then written high again during init/sleep(False))
    assert call(0x74, 0x0A, 0x01) in i2c_bus.write_byte_data.call_args_list


def test_hide(i2c_bus):
    device = scrollphathd(i2c_bus)
    i2c_bus.reset_mock()
    device.hide()
    i2c_bus.write_byte_data.assert_any_call(0x74, 0x0A, 0x00)


def test_show(i2c_bus):
    device = scrollphathd(i2c_bus)
    device.hide()
    i2c_bus.reset_mock()
    device.show()
    i2c_bus.write_byte_data.assert_any_call(0x74, 0x0A, 0x01)


def test_display_single_pixel(i2c_bus):
    device = scrollphathd(i2c_bus)
    i2c_bus.reset_mock()

    with canvas(device) as draw:
        draw.point((0, 0), fill="white")

    expected = blank_pwm()
    expected[device._pixel_address(0, 0)] = 0x70  # default contrast level

    for offset in range(0, NUM_PIXELS, 32):
        chunk = expected[offset:offset + 32]
        i2c_bus.write_i2c_block_data.assert_any_call(0x74, 0x24 + offset, chunk)


def test_display_alpha_sets_brightness(i2c_bus):
    device = scrollphathd(i2c_bus)
    i2c_bus.reset_mock()

    with canvas(device) as draw:
        draw.point((3, 2), fill=(0xFF, 0xFF, 0xFF, 0x40))

    expected = blank_pwm()
    expected[device._pixel_address(3, 2)] = 0x40

    for offset in range(0, NUM_PIXELS, 32):
        chunk = expected[offset:offset + 32]
        i2c_bus.write_i2c_block_data.assert_any_call(0x74, 0x24 + offset, chunk)


def test_display_uses_max_channel_for_intensity(i2c_bus):
    device = scrollphathd(i2c_bus)
    device.contrast(0xFF)
    i2c_bus.reset_mock()

    with canvas(device) as draw:
        draw.point((1, 1), fill=(0x10, 0x99, 0x40))

    expected = blank_pwm()
    expected[device._pixel_address(1, 1)] = 0x99

    for offset in range(0, NUM_PIXELS, 32):
        chunk = expected[offset:offset + 32]
        i2c_bus.write_i2c_block_data.assert_any_call(0x74, 0x24 + offset, chunk)


def test_contrast_redisplays_last_image(i2c_bus):
    device = scrollphathd(i2c_bus)
    with canvas(device) as draw:
        draw.point((0, 0), fill="white")
    i2c_bus.reset_mock()

    device.contrast(0xFF)

    expected = blank_pwm()
    expected[device._pixel_address(0, 0)] = 0xFF
    i2c_bus.write_i2c_block_data.assert_any_call(0x74, 0x24, expected[0:32])


def test_pixel_address_mapping_is_bijective():
    seen = set()
    for y in range(7):
        for x in range(17):
            addr = scrollphathd._pixel_address(x, y)
            assert 0 <= addr < NUM_PIXELS
            assert addr not in seen
            seen.add(addr)
    assert len(seen) == 119
