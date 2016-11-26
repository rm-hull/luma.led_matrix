Introduction
------------
Interfacing LED matrix displays with the MAX7219 driver :download:`[PDF datasheet] <MAX7219-datasheet.pdf>`
in Python (both 2.7 and 3.4 are supported) using hardware SPI on the Raspberry Pi. A LED matrix can
be acquired for a few pounds from outlets like 
`Banggood <http://www.banggood.com/MAX7219-Dot-Matrix-Module-DIY-Kit-SCM-Control-Module-For-Arduino-p-72178.html?currency=GBP>`_.
Likewise 7-segment displays are available from
`Ali-Express <http://www.aliexpress.com/item/MAX7219-Red-Module-8-Digit-7-Segment-Digital-LED-Display-Tube-For-Arduino-MCU/1449630475.html>`_
or `Ebay <http://www.ebay.com/itm/-/172317726225>`_.

This library supports:

* multiple cascaded devices
* LED matrix and seven-segment variants

.. image:: images/devices.jpg
   :alt: max7219 matrix
