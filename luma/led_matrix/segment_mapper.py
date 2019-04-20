# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

_DIGITS = {
    ' ': 0x00,
    '!': 0xa0,
    '"': 0x22,
    '#': 0x3f,
    '$': 0x5b,
    '%': 0xa5,
    "'": 0x02,
    '(': 0x4e,
    ')': 0x78,
    '*': 0x49,
    '+': 0x07,
    ',': 0x80,
    '-': 0x01,
    '.': 0x80,
    '/': 0x25,
    '0': 0x7e,
    '1': 0x30,
    '2': 0x6d,
    '3': 0x79,
    '4': 0x33,
    '5': 0x5b,
    '6': 0x5f,
    '7': 0x70,
    '8': 0x7f,
    '9': 0x7b,
    ':': 0x48,
    ';': 0x58,
    '<': 0x0d,
    '=': 0x09,
    '>': 0x19,
    '?': 0xe5,
    '@': 0x6f,
    'A': 0x77,
    'B': 0x7f,
    'C': 0x4e,
    'D': 0x7e,
    'E': 0x4f,
    'F': 0x47,
    'G': 0x5e,
    'H': 0x37,
    'I': 0x30,
    'J': 0x38,
    'K': 0x57,
    'L': 0x0e,
    'M': 0x54,
    'N': 0x76,
    'O': 0x7e,
    'P': 0x67,
    'Q': 0x73,
    'R': 0x46,
    'S': 0x5b,
    'T': 0x0f,
    'U': 0x3e,
    'V': 0x3e,
    'W': 0x2a,
    'X': 0x37,
    'Y': 0x3b,
    'Z': 0x6d,
    '[': 0x43,
    '\\': 0x13,
    ']': 0x61,
    '^': 0x62,
    '_': 0x08,
    '`': 0x20,
    'a': 0x7d,
    'b': 0x1f,
    'c': 0x0d,
    'd': 0x3d,
    'e': 0x6f,
    'f': 0x47,
    'g': 0x7b,
    'h': 0x17,
    'i': 0x10,
    'j': 0x18,
    'k': 0x57,
    'l': 0x06,
    'm': 0x14,
    'n': 0x15,
    'o': 0x1d,
    'p': 0x67,
    'q': 0x73,
    'r': 0x05,
    's': 0x5b,
    't': 0x0f,
    'u': 0x1c,
    'v': 0x1c,
    'w': 0x14,
    'x': 0x37,
    'y': 0x3b,
    'z': 0x6d,
    '{': 0x31,
    '|': 0x06,
    '}': 0x07,
    '~': 0x40,
    u'°': 0x63,
    u'\xb0': 0x63,
}


def regular(text, notfound="_"):
    undefined = _DIGITS[notfound] if notfound is not None else None
    for char in iter(text):
        digit = _DIGITS.get(char, undefined)
        if digit is not None:
            yield digit


def dot_muncher(text, notfound="_"):
    if not text:
        return

    undefined = _DIGITS[notfound] if notfound is not None else None
    last = None
    for char in iter(text):
        curr = _DIGITS.get(char, undefined)

        if curr == 0x80:
            yield curr | (last or 0)
        elif last != 0x80 and last is not None:
            yield last

        last = curr

    if curr != 0x80 and curr is not None:
        yield curr
