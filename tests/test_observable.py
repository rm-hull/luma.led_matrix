#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.


from luma.led_matrix.device import observable


class test_bell(object):

    called = 0

    def ding(self, *args):
        self.called += 1


def test_length():
    bell = test_bell()
    buf = observable(bytearray("hello", "utf-8"), bell.ding)
    assert len(buf) == 5
    assert bell.called == 1


def test_iteration():
    bell = test_bell()
    buf = observable(bytearray("hello", "utf-8"), bell.ding)
    assert list(iter(buf)) == [ord(ch) for ch in "hello"]
    assert bell.called == 1


def test_getattribute():
    bell = test_bell()
    buf = observable(bytearray("hello", "utf-8"), bell.ding)
    assert list(iter(buf.decode("utf-8"))) == list("hello")
    assert bell.called == 1


def test_getitem():
    bell = test_bell()
    buf = observable(bytearray("hello", "utf-8"), bell.ding)
    assert buf[2] == ord("l")
    assert bell.called == 1


def test_setitem():
    bell = test_bell()
    buf = observable(bytearray("hello", "utf-8"), bell.ding)
    buf[0] = ord("y")
    assert buf.decode("utf-8") == "yello"
    assert bell.called == 2


def test_setslice():
    bell = test_bell()
    buf = observable(bytearray("hello", "utf-8"), bell.ding)
    buf[1:4] = "app"
    assert buf.decode("utf-8") == "happo"
    assert bell.called == 2


def test_delitem():
    bell = test_bell()
    buf = observable(bytearray("hello", "utf-8"), bell.ding)
    del buf[4]
    assert buf.decode("utf-8") == "hell"
    assert bell.called == 2


def test_getslice():
    bell = test_bell()
    buf = observable(bytearray("hello", "utf-8"), bell.ding)
    assert buf[2:4] == bytearray("ll", "utf-8")
    assert bell.called == 1


def test_repr():
    bell = test_bell()
    buf = observable(bytearray("hello", "utf-8"), bell.ding)
    assert repr(buf) == "bytearray(b'hello')"
    assert bell.called == 1
