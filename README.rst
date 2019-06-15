`luma.core <https://github.com/rm-hull/luma.core>`__ **|** 
`luma.docs <https://github.com/rm-hull/luma.docs>`__ **|** 
`luma.emulator <https://github.com/rm-hull/luma.emulator>`__ **|** 
`luma.examples <https://github.com/rm-hull/luma.examples>`__ **|** 
`luma.lcd <https://github.com/rm-hull/luma.lcd>`__ **|** 
luma.led_matrix **|** 
`luma.oled <https://github.com/rm-hull/luma.oled>`__ 

Luma.LED_Matrix 
===============
**Display drivers for MAX7219, WS2812, APA102**

.. image:: https://travis-ci.org/rm-hull/luma.led_matrix.svg?branch=master
   :target: https://travis-ci.org/rm-hull/luma.led_matrix

.. image:: https://coveralls.io/repos/github/rm-hull/luma.led_matrix/badge.svg?branch=master
   :target: https://coveralls.io/github/rm-hull/luma.led_matrix?branch=master

.. image:: https://readthedocs.org/projects/luma-led_matrix/badge/?version=latest
   :target: http://luma-led-matrix.readthedocs.io/en/latest/?badge=latest

.. image:: https://img.shields.io/pypi/pyversions/luma.led_matrix.svg
   :target: https://pypi.python.org/pypi/luma.led_matrix

.. image:: https://img.shields.io/pypi/v/luma.led_matrix.svg
   :target: https://pypi.python.org/pypi/luma.led_matrix

.. image:: https://img.shields.io/maintenance/yes/2019.svg?maxAge=2592000

Python library interfacing LED matrix displays with the MAX7219 driver (using
SPI) and WS2812 & APA102 NeoPixels (inc Pimoroni Unicorn pHat/Hat and Unicorn
Hat HD) on the Raspberry Pi and other Linux-based single board computers - it
provides a Pillow-compatible drawing canvas, and other functionality to
support:

* multiple cascaded devices
* LED matrix, seven-segment and NeoPixel variants
* scrolling/panning capability,
* terminal-style printing,
* state management,
* dithering to monochrome,
* pygame emulator,
* Python 2.7 and 3.4+ are both supported

Documentation
-------------
Full documentation with installation instructions and examples can be found on https://luma-led-matrix.readthedocs.io.

.. image:: https://raw.githubusercontent.com/rm-hull/luma.led_matrix/master/doc/images/devices.jpg
   :alt: max7219 matrix

A LED matrix can be acquired for a few pounds from outlets
like `Banggood <http://www.banggood.com/MAX7219-Dot-Matrix-Module-DIY-Kit-SCM-Control-Module-For-Arduino-p-72178.html?currency=GBP>`_.
Likewise 7-segment displays are available from `Ali-Express
<http://www.aliexpress.com/item/MAX7219-Red-Module-8-Digit-7-Segment-Digital-LED-Display-Tube-For-Arduino-MCU/1449630475.html>`_
or `Ebay <http://www.ebay.com/itm/-/172317726225>`_.

.. image:: https://raw.githubusercontent.com/rm-hull/luma.led_matrix/master/doc/images/IMG_2810.JPG
   :alt: max7219 sevensegment

.. image:: https://raw.githubusercontent.com/rm-hull/luma.led_matrix/master/doc/images/matrix_cascaded.jpg
   :alt: max7219 cascaded
 
.. image:: https://raw.githubusercontent.com/rm-hull/luma.led_matrix/master/doc/images/box_helloworld.jpg
   :alt: max7219 box
     
.. image:: https://raw.githubusercontent.com/rm-hull/luma.led_matrix/master/doc/images/emulator.gif
   :alt: max7219 emulator

Breaking changes
----------------
Version 0.3.0 was released on 19 January 2017: this came with a rename of the
github project from **max7219** to **luma.led_matrix** to reflect the changing
nature of the codebase.

There is no direct migration path, but the old `docs <https://max7219.readthedocs.io>`_
and `PyPi packages <https://pypi.python.org/pypi/max7219>`_ will remain
available indefinitely, but that deprecated codebase will no longer recieve 
updates or fixes.

The consequence is that any existing code that uses the old **max7219** package
should probably be updated. 

License
-------
The MIT License (MIT)

Copyright (c) 2013-2019 Richard Hull & Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
