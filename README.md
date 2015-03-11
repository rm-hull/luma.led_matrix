MAX7219 Driver
==============

Interfacing LED matrix displays with the MAX7219 driver 
[[PDF datasheet](https://raw.github.com/rm-hull/max7219/master/docs/MAX7219-datasheet.pdf)] 
in Python using hardware SPI on the Raspberry Pi. The particular LED matrix I bought 
can be acquired for a few pounds from 
[Banggood](http://www.banggood.com/MAX7219-Dot-Matrix-Module-DIY-Kit-SCM-Control-Module-For-Arduino-p-72178.html?currency=GBP).
Likewise 7-segment displays are available from [Ali-Express](http://www.aliexpress.com/item/MAX7219-Red-Module-8-Digit-7-Segment-Digital-LED-Display-Tube-For-Arduino-MCU/1449630475.html).
There are many other outlets selling both types of devices on Ebay and other such places.

This library has recently had a major overhaul, and is not compatible with the earlier version. 
It now supports:

* multiple cascaded devices
* LED matrix and seven-segement variants

![max7219 matrix](https://raw.githubusercontent.com/rm-hull/max7219/master/docs/images/devices.jpg)

Python Usage
------------
For the matrix device, initialize the `matrix` class:

```python
import max7219.led as led

device = led.matrix()
device.show_message("Hello world!")
```

For the 7-segment devce, initialize the `sevensegment` class:

```python
import max7219.led as led

device = led.sevensegment()
device.write_number(deviceId=0, value=3.14159)
```

The MAX7219 chipset supports a serial 16-bit register/data buffer which is 
clocked in on pin DIN every time the clock edge falls, and clocked out on DOUT
16.5 clock cycles later. This allows multiple devices to be chained together.

When initializing cascaded devices, it is necessary to specify a `cascaded=...`
parameter, and generally methods which target specific devices will expect a 
`deviceId=...` parameter, counting from zero.

For more information, see http://max7219.readthedocs.org/

![max7219 sevensegment](https://raw.githubusercontent.com/rm-hull/max7219/master/docs/images/IMG_2810.JPG)

Pre-requisites
--------------
Ensure that the SPI kernel driver is enabled:

    $ dmesg | grep spi
    [    3.769841] bcm2708_spi bcm2708_spi.0: master is unqueued, this is deprecated
    [    3.793364] bcm2708_spi bcm2708_spi.0: SPI Controller at 0x20204000 (irq 80)

And that the devices are successfully installed in /dev:

    $ ls -l /dev/spi*
    crw------- 1 root root 153, 0 Jan  1  1970 /dev/spidev0.0
    crw------- 1 root root 153, 1 Jan  1  1970 /dev/spidev0.1
    
Follow the advice in the references below if the devices do not appear before
proceeding.

GPIO pin-outs
-------------
The breakout board has an two headers to allow daisy-chaining:

| Board Pin | Name | Remarks | RPi Pin | RPi Function |
|--------:|:-----|:--------|--------:|--------------|
| 1 | VCC | +5V Power | 2 | 5V0 |
| 2 | GND | Ground | 6 | GND |
| 3 | DIN | Data In | 19 | GPIO 10 (MOSI) |
| 4 | CS | Chip Select | 24 | GPIO 8 (SPI CE0) |
| 5 | CLK | Clock | 23 | GPIO 11 (SPI CLK) |

Building & Installing
---------------------
For Raspian:

On setup while in raspbian config or post install by running 'sudo raspi-config' you must enable SPI: 8 Advanced options > A6 SPI > Yes (Would you like the SPI interface enabled?) > OK > Yes (Would you like the SPI kernel module to be loaded by default?) > OK  

    $ sudo apt-get install python-dev python-pip
    $ sudo pip install spidev
    $ sudo python setup.py install

For Arch Linux:

    # pacman -Sy base-devel python2
    # pip install spidev
    # python2 setup.py install


Examples
--------
Run the example code as follows:

    $ sudo python examples/matrix_test.py

or

    $ sudo python examples/sevensegment_test.py

*NOTE:* By default, SPI is only accessible by root (hence using `sudo` above). Follow these 
instructions to create an spi group, and adding your user to that group, so you don't have to
run as root: http://quick2wire.com/non-root-access-to-spi-on-the-pi

References
----------
* http://hackaday.com/2013/01/06/hardware-spi-with-python-on-a-raspberry-pi/
* http://gammon.com.au/forum/?id=11516
* http://louisthiery.com/spi-python-hardware-spi-for-raspi/
* http://www.brianhensley.net/2012/07/getting-spi-working-on-raspberry-pi.html
* http://raspi.tv/2013/8-x-8-led-array-driven-by-max7219-on-the-raspberry-pi-via-python
* http://quick2wire.com/non-root-access-to-spi-on-the-pi

License
-------
See [MIT License](https://github.com/rm-hull/max7219/blob/master/LICENSE.md).
