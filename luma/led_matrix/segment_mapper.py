# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.

_DIGITS = {
    ' ': 0x00,
    '-': 0x01,
    '_': 0x08,
    '\'': 0x02,
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
    # 'k': cant represent
    'l': 0x06,
    # 'm': cant represent
    'n': 0x15,
    'o': 0x1d,
    'p': 0x67,
    'q': 0x73,
    'r': 0x05,
    's': 0x5b,
    't': 0x0f,
    'u': 0x1c,
    'v': 0x1c,
    # 'w': cant represent
    # 'x': cant represent
    'y': 0x3b,
    'z': 0x6d,
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
    # 'K': cant represent
    'L': 0x0e,
    # 'M': cant represent
    'N': 0x76,
    'O': 0x7e,
    'P': 0x67,
    'Q': 0x73,
    'R': 0x46,
    'S': 0x5b,
    'T': 0x0f,
    'U': 0x3e,
    'V': 0x3e,
    # 'W': cant represent
    # 'X': cant represent
    'Y': 0x3b,
    'Z': 0x6d,
    ',': 0x80,
    '.': 0x80
}


def regular(text, notfound="_"):
    try:
        undefined = _DIGITS[notfound]
        iterator = iter(text)
        while True:
            char = next(iterator)
            yield _DIGITS.get(char, undefined)
    except StopIteration:
        pass


def dot_muncher(text, notfound="_"):
    undefined = _DIGITS[notfound]
    iterator = iter(text)
    last = _DIGITS.get(next(iterator), undefined)
    try:
        while True:
            curr = _DIGITS.get(next(iterator), undefined)

            if curr == 0x80:
                yield curr | last
            elif last != 0x80:
                yield last

            last = curr
    except StopIteration:
        if last != 0x80:
            yield last
