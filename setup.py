#!/usr/bin/env python

from distutils.core import setup,Extension
setup(
    name = "max7219",
    version = "0.0.1",
    author = "Richard Hull",
    author_email = "richard.hull@destructuring-bind.org",
    description = ("A small library to drive a MAX7219 LED serializer using hardware SPI-Py"),
    license = "GPLv2",
    keywords = "raspberry pi rpi led max7219",
    url = "https://github.com/rm-hull/max7219",
    packages=['max7219'],
    package_dir={'max7219': 'src'},
    ext_modules=[Extension('max7219.spi',['src/spi.c'])]
)
