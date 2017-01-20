#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.


from luma.led_matrix.legacy import proportional, CP437_FONT


def test_narrow_char():
    font = proportional(CP437_FONT)
    assert font[ord('!')] == [6, 95, 95, 6, 0]


def test_wide_char():
    font = proportional(CP437_FONT)
    assert font[ord('W')] == CP437_FONT[ord('W')]


def test_space_char():
    font = proportional(CP437_FONT)
    assert font[ord(' ')] == CP437_FONT[ord(' ')]


def test_doublequote_char():
    font = proportional(CP437_FONT)
    assert font[ord('"')] == [7, 7, 0, 7, 7, 0]
