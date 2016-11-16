#!/usr/bin/env python

import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()
version = "0.2.3"

setup(
    name="max7219",
    version=version,
    author="Richard Hull",
    author_email="richard.hull@destructuring-bind.org",
    description="A library to drive a MAX7219 LED serializer using hardware spidev",
    long_description=README,
    license="MIT",
    keywords=["raspberry pi", "rpi", "led", "max7219", "matrix", "seven segment", "7 segment"],
    url="https://github.com/rm-hull/max7219",
    download_url="https://github.com/rm-hull/max7219/tarball/" + version,
    packages=["max7219"],
    install_requires=["spidev"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Topic :: Education",
        "Topic :: System :: Hardware",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ]
)
