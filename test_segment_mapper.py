#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.


from luma.led_matrix.segment_mapper import dot_muncher, regular


def test_dot_muncher_without_dots():
    buf = bytearray("Hello world", "utf-8")
    results = dot_muncher(buf)
    assert list(results) == [0x37, 0x6f, 0x06, 0x06, 0x1d, 0x00, 0x08, 0x1d, 0x05, 0x06, 0x3d]


def test_dot_muncher_with_dot():
    buf = bytearray("3.14159", "utf-8")
    results = dot_muncher(buf)
    assert list(results) == [0x79 | 0x80, 0x30, 0x33, 0x30, 0x5b, 0x7b]


def test_dot_muncher_with_multiple_dot():
    buf = bytearray("127.0.0.1", "utf-8")
    results = dot_muncher(buf)
    assert list(results) == [0x30, 0x6d, 0x70 | 0x80, 0x7e | 0x80, 0x7e | 0x80, 0x30]


def test_dot_muncher_empty_buf():
    buf = bytearray("", "utf-8")
    results = dot_muncher(buf)
    assert list(results) == []


def test_regular_without_dots():
    buf = bytearray("Hello world", "utf-8")
    results = regular(buf)
    assert list(results) == [0x37, 0x6f, 0x06, 0x06, 0x1d, 0x00, 0x08, 0x1d, 0x05, 0x06, 0x3d]


def test_regular_with_dot():
    buf = bytearray("3.14159", "utf-8")
    results = regular(buf)
    assert list(results) == [0x79, 0x80, 0x30, 0x33, 0x30, 0x5b, 0x7b]


def test_regular_with_multiple_dot():
    buf = bytearray("127.0.0.1", "utf-8")
    results = regular(buf)
    assert list(results) == [0x30, 0x6d, 0x70, 0x80, 0x7e, 0x80, 0x7e, 0x80, 0x30]


def test_regular_empty_buf():
    buf = bytearray("", "utf-8")
    results = regular(buf)
    assert list(results) == []
