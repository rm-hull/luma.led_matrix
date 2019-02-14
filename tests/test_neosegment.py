#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import pytest

from PIL import Image

from luma.led_matrix.device import neosegment
from luma.core.device import dummy
from luma.core.render import canvas
import luma.core.error

from helpers import assert_identical_image, get_reference_image


def test_invalid_dimensions():
    with pytest.raises(luma.core.error.DeviceDisplayModeError) as ex:
        neosegment(width=3, device=dummy(width=6, height=7))
    assert "Unsupported display mode: width=3" in str(ex.value)


def test_overflow():
    with pytest.raises(OverflowError) as ex:
        neoseg = neosegment(width=6, device=dummy(width=6, height=7))
        neoseg.text = "TooBig!"
    assert "Device's capabilities insufficient for value 'TooBig!'" in str(ex.value)


def test_settext_nocolor():
    neoseg = neosegment(width=6, device=dummy(width=6, height=7))
    neoseg.text = "888888"
    ref = dummy(width=6, height=7)
    with canvas(ref) as draw:
        draw.rectangle(ref.bounding_box, fill="white")
    assert_identical_image(ref.image, neoseg.device.image)


def test_settext_singlecolor():
    neoseg = neosegment(width=6, device=dummy(width=6, height=7))
    neoseg.text = "888888"
    neoseg.color = "red"
    ref = dummy(width=6, height=7)
    with canvas(ref) as draw:
        draw.rectangle(ref.bounding_box, fill="red")
    assert_identical_image(ref.image, neoseg.device.image)


def test_settext_charcolor():
    neoseg = neosegment(width=6, device=dummy(width=6, height=7))
    neoseg.text = "888888"
    neoseg.color[2] = "green"
    ref = dummy(width=6, height=7)
    with canvas(ref) as draw:
        draw.rectangle(ref.bounding_box, fill="white")
        draw.rectangle([2, 0, 2, 6], fill="green")
    assert_identical_image(ref.image, neoseg.device.image)


def test_settext_replacechars():
    neoseg = neosegment(width=6, device=dummy(width=6, height=7))
    neoseg.text = "888888"
    neoseg.text[2:4] = "  "
    ref = dummy(width=6, height=7)
    with canvas(ref) as draw:
        draw.rectangle(ref.bounding_box, fill="white")
        draw.rectangle([2, 0, 3, 6], fill="black")
    assert_identical_image(ref.image, neoseg.device.image)


def test_segment_mapper():
    img_path = get_reference_image('neosegment.png')

    with open(img_path, 'rb') as img:
        reference = Image.open(img)
        neoseg = neosegment(width=6, device=dummy(width=6, height=7))
        neoseg.color = ["red", "green", "blue", "yellow", "cyan", "magenta"]
        neoseg.text = "012345"
        assert_identical_image(reference, neoseg.device.image)


def test_unknown_char():
    neoseg = neosegment(width=6, device=dummy(width=6, height=7))
    neoseg.text = "888888"
    neoseg.text[2:4] = "&\x7f"
    neoseg.color[2:4] = ["orange", "orange"]
    ref = dummy(width=6, height=7)
    with canvas(ref) as draw:
        draw.rectangle(ref.bounding_box, fill="white")
        draw.rectangle([2, 0, 3, 6], fill="black")
        draw.rectangle([2, 1, 3, 1], fill="orange")
    assert_identical_image(ref.image, neoseg.device.image)
