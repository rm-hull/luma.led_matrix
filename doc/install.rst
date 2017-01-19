Installation
------------
.. note:: The library has been tested against Python 2.7 and 3.4+.

   For **Python3** installation, substitute the following in the 
   instructions below.

   * ``pip`` ⇒ ``pip3``, 
   * ``python`` ⇒ ``python3``, 
   * ``python-dev`` ⇒ ``python3-dev``,
   * ``python-pip`` ⇒ ``python3-pip``.

Pre-requisites
^^^^^^^^^^^^^^
By default, the SPI kernel driver is **NOT** enabled on the Raspberry Pi Raspian image.
You can confirm whether it is enabled using the shell commands below::

  $ lsmod | grep -i spi
  spi_bcm2835             7424  0

Depending on the hardware/kernel version, this may report **spi_bcm2807** rather 
than **spi_bcm2835** - either should be adequate.

And that the devices are successfully installed in ``/dev``::

  $ ls -l /dev/spi*
  crw------- 1 root root 153, 0 Jan  1  1970 /dev/spidev0.0
  crw------- 1 root root 153, 1 Jan  1  1970 /dev/spidev0.1

If you have no ``/dev/spi`` files and nothing is showing using ``lsmod`` then this
implies the kernel SPI driver is not loaded. Enable the SPI as follows (steps
taken from https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial#spi-on-pi):

#. Run ``sudo raspi-config``
#. Use the down arrow to select ``9 Advanced Options``
#. Arrow down to ``A6 SPI.``
#. Select **yes** when it asks you to enable SPI,
#. Also select **yes** when it asks about automatically loading the kernel module.
#. Use the right arrow to select the **<Finish>** button.
#. Select **yes** when it asks to reboot.

.. image:: images/raspi-spi.png

After rebooting re-check that the ``lsmod | grep -i spi`` command shows whether
SPI driver is loaded before proceeding. If you are stil experiencing problems, refer to the official 
Raspberry Pi `SPI troubleshooting guide <https://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md#troubleshooting>`_
for further details, or ask a `new question <https://github.com/rm-hull/luma.led_matrix/issues/new>`_ - but
please remember to add as much detail as possible.

GPIO pin-outs
^^^^^^^^^^^^^
The breakout board has two headers to allow daisy-chaining:

============ ====== ============= ========= ====================
Board Pin    Name   Remarks       RPi Pin   RPi Function
------------ ------ ------------- --------- --------------------
1            VCC    +5V Power     2         5V0
2            GND    Ground        6         GND
3            DIN    Data In       19        GPIO 10 (MOSI)
4            CS     Chip Select   24        GPIO 8 (SPI CE0)
5            CLK    Clock         23        GPIO 11 (SPI CLK)
============ ====== ============= ========= ====================

.. seealso:: See below for cascading/daisy-chaining, power supply and level-shifting.

Installing from PyPi
^^^^^^^^^^^^^^^^^^^^
.. note:: This is the preferred installation mechanism.

Install the latest version of the library directly from
`PyPI <https://pypi.python.org/pypi?:action=display&name=luma.led_matrix>`_::

  $ sudo apt-get install python-dev python-pip
  $ sudo pip install --upgrade luma.led_matrix

Installing from source
^^^^^^^^^^^^^^^^^^^^^^
Alternatively, clone the code from github::

  $ git clone https://github.com/rm-hull/luma.led_matrix.git

Next, follow the specific steps below for your OS.

Raspbian
""""""""
.. code:: bash

  $ cd luma.led_matrix
  $ sudo apt-get install python-dev python-pip
  $ sudo pip install spidev
  $ sudo python setup.py install

Arch Linux
""""""""""
.. code:: bash

  cd luma.led_matrix
  pacman -Sy base-devel python2
  pip install spidev
  python2 setup.py install
