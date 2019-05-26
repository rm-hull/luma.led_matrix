#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-19 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Collection of datasets to prevent regression bugs from creeping in.
"""

import io
import json
import os.path


def get_json_data(fname):
    dirname = os.path.abspath(os.path.dirname(__file__))
    fpath = os.path.join(dirname, 'reference', 'data', fname + '.json')
    with io.open(fpath) as f:
        return json.load(f)
