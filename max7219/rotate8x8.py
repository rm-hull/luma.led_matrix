#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A python port of:
#   http://tog.acm.org/resources/GraphicsGems/gemsii/rotate8x8.c
#
# Originally written in C by: Ken Yap (Centre for Spatial Information Systems,
# CSIRO DIT, Australia) after an idea suggested by Alan Paeth (U of Waterloo).
#


def _table(n):
    return [x << n for x in [
        0x00000000, 0x00000001, 0x00000100, 0x00000101,
        0x00010000, 0x00010001, 0x00010100, 0x00010101,
        0x01000000, 0x01000001, 0x01000100, 0x01000101,
        0x01010000, 0x01010001, 0x01010100, 0x01010101]]

ltab = [_table(i) for i in range(7, -1, -1)]


def rotate(src):
    """
    Rotate an 8x8 tile (8-element array of 8-bit numbers) 90 degrees
    counter-clockwise by table lookup. Large bitmaps can be rotated
    an 8x8 tile at a time. The extraction is done a nybble at a time
    to reduce the size of the tables.
    """
    assert len(src) == 8

    low = 0
    hi = 0

    # Extract
    for i in range(8):
        value = src[i]
        assert 0 <= value < 256, 'src[{0}] {1} outside range 0..255'.format(i, value)

        low |= ltab[i][value & 0x0f]
        hi |= ltab[i][value >> 4]

    # Unpack
    return [int(val >> i & 0xff) for val in [low, hi] for i in [0, 8, 16, 24]]
