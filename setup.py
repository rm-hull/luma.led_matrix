#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()
CONTRIB = open(os.path.join(os.path.dirname(__file__), "CONTRIBUTING.rst")).read()
CHANGES = open(os.path.join(os.path.dirname(__file__), "CHANGES.rst")).read()
version = open(os.path.join(os.path.dirname(__file__), "VERSION.txt")).read().strip()

setup(
    name="luma.led_matrix",
    version=version,
    author="Richard Hull",
    author_email="richard.hull@destructuring-bind.org",
    description="A library to drive a MAX7219 LED serializer (using SPI) and WS2812 NeoPixels (using DMA)",
    long_description="\n\n".join([README, CONTRIB, CHANGES]),
    license="MIT",
    keywords=["raspberry pi", "rpi", "led", "max7219", "matrix", "seven segment", "7 segment", "neopixel", "ws2812", "ws281x"],
    url="https://github.com/rm-hull/luma.led_matrix",
    download_url="https://github.com/rm-hull/luma.led_matrix/tarball/" + version,
    namespace_packages=["luma"],
    packages=["luma.led_matrix"],
    install_requires=["luma.core>=0.3.1", "ws2812"],
    setup_requires=["pytest-runner"],
    tests_require=["mock", "pytest", "pytest-cov", "python-coveralls"],
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Education",
        "Topic :: System :: Hardware",
        "Topic :: System :: Hardware :: Hardware Drivers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Operating System :: POSIX",
        "Operating System :: Unix"
    ]
)
