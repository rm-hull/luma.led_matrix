# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import os.path

try:
    from unittest.mock import call, Mock
except ImportError:
    from mock import call, Mock  # noqa: F401

import pytest
from PIL import ImageChops

import luma.core.error

serial = Mock(unsafe=True)


def setup_function(function):
    """
    Called after a test finished.
    """
    serial.reset_mock()
    serial.command.side_effect = None


def assert_invalid_dimensions(deviceType, serial_interface, width, height):
    """
    Assert an invalid resolution raises a
    :py:class:`luma.core.error.DeviceDisplayModeError`.
    """
    with pytest.raises(luma.core.error.DeviceDisplayModeError) as ex:
        deviceType(serial_interface, width=width, height=height)
    assert "Unsupported display mode: {} x {}".format(width, height) in str(ex.value)


def get_reference_file(fname):
    return os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        'reference',
        fname))


def get_reference_image(fname):
    return get_reference_file(os.path.join('images', fname))


def assert_identical_image(reference, target):
    bbox = ImageChops.difference(reference, target).getbbox()
    assert bbox is None
