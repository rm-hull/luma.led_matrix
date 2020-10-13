#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2020 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Collection of datasets to prevent regression bugs from creeping in.
"""

import json
from pathlib import Path


def get_json_data(fname):
    """
    Load JSON reference data.

    :param fname: Filename without extension.
    :type fname: str
    """
    base_dir = Path(__file__).resolve().parent
    fpath = base_dir.joinpath('reference', 'data', fname + '.json')
    with fpath.open() as f:
        return json.load(f)
