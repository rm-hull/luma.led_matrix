Using MAX7219 Driver for a seven segment display
================================================

Using the MAX7219 driver in Python for a 8 digit seven segment LED display (MAX7219 based of course).

Eg: (but not limited to)
http://www.aliexpress.com/item/MAX7219-Red-Module-8-Digit-7-Segment-Digital-LED-Display-Tube-For-Arduino-MCU/1449630475.html

![max7219 7segment](https://raw.github.com/rm-hull/max7219/master/doc/images/7segment.jpg)

Library
-------
sevenSegment.py

based on some Ardafruit Libs to allow Raw interaction, display hex digits on a particular column or printing decimal values without taking care of the positions

Examples
--------
demo: some library demonstration

sevenClock: a clock (hh:mm) with a blinking decimal point as delimiter

counter: a increasing counter

/Reimer Prochnow
