# -*- coding: utf-8 -*-
# Copyright (c) 2017-2020 Richard Hull and contributors
# See LICENSE.rst for details.

from pathlib import Path
from unittest.mock import Mock

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
    assert f"Unsupported display mode: {width} x {height}" in str(ex.value)


def get_reference_file(fname):
    """
    Get absolute path for ``fname``.

    :param fname: Filename.
    :type fname: str or pathlib.Path
    :rtype: str
    """
    return str(Path(__file__).resolve().parent.joinpath('reference', fname))


def get_reference_image(fname):
    """
    :param fname: Filename.
    :type fname: str or pathlib.Path
    """
    return get_reference_file(Path('images').joinpath(fname))


def assert_identical_image(reference, target):
    bbox = ImageChops.difference(reference, target).getbbox()
    assert bbox is None
