#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-18 Richard Hull and contributors
# See LICENSE.rst for details.


from luma.core.util import mutable_string
from luma.led_matrix.segment_mapper import dot_muncher, regular


def test_dot_muncher_without_dots():
    buf = mutable_string("Hello world")
    results = dot_muncher(buf, notfound='_')
    assert list(results) == [0x37, 0x6f, 0x06, 0x06, 0x1d, 0x00, 0x14, 0x1d, 0x05, 0x06, 0x3d]


def test_dot_muncher_with_dot():
    buf = mutable_string("3.14159")
    results = dot_muncher(buf)
    assert list(results) == [0x79 | 0x80, 0x30, 0x33, 0x30, 0x5b, 0x7b]


def test_dot_muncher_with_dot_at_end():
    buf = mutable_string("  525920")
    buf[7:] = "0."
    print(buf)
    results = dot_muncher(buf)
    assert list(results) == [0x00, 0x00, 0x5b, 0x6d, 0x5b, 0x7b, 0x6d, 0x7e | 0x80]


def test_dot_muncher_with_dot_at_start():
    buf = mutable_string(".PDF")
    results = dot_muncher(buf)
    assert list(results) == [0x80, 0x67, 0x7e, 0x47]


def test_dot_muncher_with_multiple_dot():
    buf = mutable_string("127.0.0.1")
    results = dot_muncher(buf)
    assert list(results) == [0x30, 0x6d, 0x70 | 0x80, 0x7e | 0x80, 0x7e | 0x80, 0x30]


def test_dot_muncher_with_consecutive_dot():
    buf = mutable_string("No...")
    results = dot_muncher(buf)
    assert list(results) == [0x76, 0x1d | 0x80, 0x80, 0x80]


def test_dot_muncher_empty_buf():
    buf = mutable_string("")
    results = dot_muncher(buf)
    assert list(results) == []


def test_dot_muncher_skips_unknown():
    buf = mutable_string("B&B")
    results = dot_muncher(buf, notfound=None)
    assert list(results) == [0x7f, 0x7f]


def test_dot_muncher_with_notfound():
    buf = mutable_string("B&B")
    results = dot_muncher(buf, notfound='_')
    assert list(results) == [0x7f, 0x08, 0x7f]


def test_regular_without_dots():
    buf = mutable_string("Hello world")
    results = regular(buf, notfound='_')
    assert list(results) == [0x37, 0x6f, 0x06, 0x06, 0x1d, 0x00, 0x14, 0x1d, 0x05, 0x06, 0x3d]


def test_regular_with_dot():
    buf = mutable_string("3.14159")
    results = regular(buf)
    assert list(results) == [0x79, 0x80, 0x30, 0x33, 0x30, 0x5b, 0x7b]


def test_regular_with_multiple_dot():
    buf = mutable_string("127.0.0.1")
    results = regular(buf)
    assert list(results) == [0x30, 0x6d, 0x70, 0x80, 0x7e, 0x80, 0x7e, 0x80, 0x30]


def test_regular_empty_buf():
    buf = mutable_string("")
    results = regular(buf)
    assert list(results) == []


def test_regular_skips_unknown():
    buf = mutable_string("B&B")
    results = regular(buf, notfound=None)
    assert list(results) == [0x7f, 0x7f]


def test_regular_with_notfound():
    buf = mutable_string("B&B")
    results = regular(buf, notfound='_')
    assert list(results) == [0x7f, 0x08, 0x7f]


def test_degrees_unicode():
    buf = mutable_string(u"29.12°C")
    results = dot_muncher(buf)
    assert list(results) == [0x6d, 0x7b | 0x80, 0x30, 0x6d, 0x63, 0x4e]


def test_degrees_utf8():
    buf = mutable_string(u"29.12\xb0C")
    results = dot_muncher(buf)
    assert list(results) == [0x6d, 0x7b | 0x80, 0x30, 0x6d, 0x63, 0x4e]
