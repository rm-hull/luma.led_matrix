#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Richard Hull and contributors
# See LICENSE.rst for details.

import warnings


def test_legacy_deprecated(recwarn):
    """
    The luma.led_matrix.legacy module is deprecated.
    """
    warnings.simplefilter('always')
    from luma.led_matrix import legacy

    assert len(recwarn) == 1
    w = recwarn.pop(DeprecationWarning)

    assert str(w.message) == legacy.deprecation_msg
