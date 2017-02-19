#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.

import pytest
import os.path

from PIL import Image, ImageChops
from luma.led_matrix.device import sevensegment
from luma.core.device import dummy


def test_init():
    device = dummy(width=24, height=8, mode="1")
    sevensegment(device)
    assert device.image == Image.new("1", (24, 8))


def test_overflow():

    device = dummy(width=24, height=8, mode="1")
    seg = sevensegment(device)
    with pytest.raises(OverflowError) as ex:
        seg.text = "This is too big to fit in 3x8 seven-segment displays"
    assert str(ex.value) == "Device's capabilities insufficent for value 'This is too big to fit in 3x8 seven-segment displays'"


def test_setter_getter():
    reference = Image.open(
        os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            'reference',
            'golden_ratio.png')))

    device = dummy(width=24, height=8)
    seg = sevensegment(device)
    seg.text = "1.61803398875"
    assert str(seg.text) == "1.61803398875"

    bbox = ImageChops.difference(reference, device.image).getbbox()
    assert bbox is None
