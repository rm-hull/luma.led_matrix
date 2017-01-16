Python Usage
------------

For the matrix device, initialize the ``matrix`` class:

.. code:: python

  import max7219.led as led

  device = led.matrix()
  device.show_message("Hello world!")

For the 7-segment device, initialize the ``sevensegment`` class:

.. code:: python

  import max7219.led as led

  device = led.sevensegment()
  device.write_number(deviceId=0, value=3.14159)

The MAX7219 chipset supports a serial 16-bit register/data buffer which is
clocked in on pin DIN every time the clock edge falls, and clocked out on DOUT
16.5 clock cycles later. This allows multiple devices to be chained together.

When initializing cascaded devices, it is necessary to specify a ``cascaded=...``
parameter, and generally methods which target specific devices will expect a
``deviceId=...`` parameter, counting from zero.

.. image:: images/IMG_2810.JPG
   :alt: max7219 sevensegment

Examples
^^^^^^^^

Ensure you have followed the installation instructions below.
Run the example code as follows::

  $ sudo python examples/matrix_test.py

or::

  $ sudo python examples/sevensegment_test.py

**Note**: By default, SPI is only accessible by root (hence using ``sudo`` above). Follow
`these instructions <http://quick2wire.com/non-root-access-to-spi-on-the-pi>`_ to create an
``spi`` group, and adding your user to that group, so you don't have to run as root.


