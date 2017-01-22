Introduction
------------
Python library interfacing LED matrix displays with the MAX7219 driver (using
SPI) and WS2812 NeoPixels (using DMA) on the Raspberry Pi and other linux-based
single board computers - it provides a Pillow-compatible drawing canvas, and
other functionality to support:

* multiple cascaded devices
* LED matrix, seven-segment and NeoPixel variants
* scrolling/panning capability,
* terminal-style printing,
* state management,
* dithering to monochrome,
* Python 2.7 and 3.4+ are both supported

.. image:: https://raw.githubusercontent.com/rm-hull/luma.led_matrix/master/doc/images/devices.jpg
   :alt: max7219 matrix

A LED matrix can be acquired for a few pounds from outlets like `Banggood
<http://www.banggood.com/MAX7219-Dot-Matrix-Module-DIY-Kit-SCM-Control-Module-For-Arduino-p-72178.html?currency=GBP>`_.
Likewise 7-segment displays are available from `Ali-Express
<http://www.aliexpress.com/item/MAX7219-Red-Module-8-Digit-7-Segment-Digital-LED-Display-Tube-For-Arduino-MCU/1449630475.html>`_
or `Ebay <http://www.ebay.com/itm/-/172317726225>`_.


