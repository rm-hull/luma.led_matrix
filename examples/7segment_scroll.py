#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-17 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
A horizontal scrolling demo, only really suitable for 7-segment LED displays.
"""

import time
from luma.core.emulator import pygame
from luma.core.virtual import viewport
from luma.led_matrix.device import sevensegment


blurb = """
Have you ever been to American wedding?
Where is the vodka, where's marinated herring?
Where is the musicians that got the taste?
Where is the supply that's gonna last three days?
Where is the band that like Fanfare.
Gonna keep it goin' 24 hours

Ta-tar-ranta-ta-ta
Super taran-ta taran-ta ran-ta ta

Instead it's one in the mornin'
and DJ is patchin' up the cords
Everybody's full of cake
Staring at the floor
Proper couples start to mumble
That it's time to do
People gotta get up early
Yep, they gotta go
People gotta get up early
And she's gotta boyfriend
And this whole fucking thing
Is just a one huge disappointment

Ta-tar-ran-ta

Nothing gets these bitches going
not even Gypsy Kings
nobody talks about my Supertheory
of Supereverythings!
So be you Donald Trump
Or be an anarchist
Make sure that your wedding
Doesn't end up like this

I understand the cultures
Of a different kind
But here word celebration
Just doesn't come to mind
"""


def main():
    device = pygame(width=24, height=8, transform="sevensegment", scale=1)
    virtual = viewport(device, width=1024, height=8)
    seg = sevensegment(virtual)

    for line in blurb.split("\n"):
        seg.text = (" " * device.width) + line
        for x in range(len(line)):
            virtual.set_position((x, 0))
            time.sleep(0.2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
