#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.


import hashlib
import os.path
from tempfile import NamedTemporaryFile
from PIL import Image

try:
    from unittest.mock import call, Mock
except ImportError:
    from mock import call, Mock

from luma.core.emulator import gifanim
from luma.led_matrix.legacy import text, show_message, textsize, proportional, CP437_FONT, LCD_FONT


def md5(fname):
    with open(fname, 'rb') as fp:
        return hashlib.md5(fp.read()).hexdigest()


def test_textsize():
    assert textsize("Hello world") == (88, 8)
    assert textsize("Hello world", font=proportional(CP437_FONT)) == (75, 8)


def test_text_space():
    draw = Mock(unsafe=True)
    text(draw, (2, 2), " ", fill="white")
    draw.point.assert_not_called()


def test_text_char():
    draw = Mock(unsafe=True)
    text(draw, (2, 2), "L", font=LCD_FONT, fill="white")
    draw.point.assert_has_calls([
        call((2, 2), fill='white'),
        call((2, 3), fill='white'),
        call((2, 4), fill='white'),
        call((2, 5), fill='white'),
        call((2, 6), fill='white'),
        call((2, 7), fill='white'),
        call((2, 8), fill='white'),
        call((3, 8), fill='white'),
        call((4, 8), fill='white'),
        call((5, 8), fill='white'),
        call((6, 8), fill='white')
    ])


def test_show_message():
    reference = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        'reference',
        'show_message.gif'))

    fname = NamedTemporaryFile(suffix=".gif").name
    device = gifanim(width=40, height=8, transform="none", filename=fname)

    show_message(device, "Hello world!", delay=0, fill="white")

    device.write_animation()

    ref = Image.open(reference)
    act = Image.open(fname)

    try:
        while True:
            assert ref == act
            ref.seek(ref.tell() + 1)
            act.seek(act.tell() + 1)
    except EOFError:
        pass
