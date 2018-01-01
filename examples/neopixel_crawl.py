#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import time

from luma.led_matrix.device import neopixel
from luma.core.render import canvas

device = neopixel(cascaded=32)

for i in range(device.cascaded):
    with canvas(device) as draw:
        draw.point((i, 0), fill="green")
    time.sleep(0.5)
