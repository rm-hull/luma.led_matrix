Raspberry PI MAX7219 driver
===========================
.. image:: https://travis-ci.org/rm-hull/max7219.svg?branch=master
   :target: https://travis-ci.org/rm-hull/max7219
   
.. image:: https://img.shields.io/pypi/v/max7219.svg
   :target: https://pypi.python.org/pypi/max7219

Interfacing LED matrix displays with the MAX7219 driver
`[PDF datasheet] <https://raw.github.com/rm-hull/max7219/master/docs/MAX7219-datasheet.pdf>`_
in Python (both 2.7 and 3.x are supported) using hardware SPI on the Raspberry Pi. A LED matrix
can be acquired for a few pounds from outlets like 
`Banggood <http://www.banggood.com/MAX7219-Dot-Matrix-Module-DIY-Kit-SCM-Control-Module-For-Arduino-p-72178.html?currency=GBP>`_.
Likewise 7-segment displays are available from
`Ali-Express <http://www.aliexpress.com/item/MAX7219-Red-Module-8-Digit-7-Segment-Digital-LED-Display-Tube-For-Arduino-MCU/1449630475.html>`_
or `Ebay <http://www.ebay.com/itm/-/172317726225>`_.

This library supports:

* multiple cascaded devices
* LED matrix and seven-segment variants

.. image:: https://raw.githubusercontent.com/rm-hull/max7219/master/docs/images/devices.jpg
   :alt: max7219 matrix

Documentation
-------------

Full documentation with installation instructions and examples can be found on https://max7219.readthedocs.io.

Contributing
------------
Pull requests (code changes / documentation / typos / feature requests / setup) are gladly accepted. If you are 
intending some large-scale changes, please get in touch first to make sure we're on the same page: try and include
a docstring for any new methods, and try and keep method bodies small, readable and PEP8-compliant.

Contributors
^^^^^^^^^^^^
* Thijs Triemstra (@thijstriemstra)
* Jon Carlos (@webmonger)
* Unattributed (@wkapga)
* Taras (@tarasius)
* Brice Parent (@agripo)

License
-------

The MIT License (MIT)

Copyright (c) 2016 Richard Hull

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
