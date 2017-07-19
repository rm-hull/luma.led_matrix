#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup


needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []


def read_file(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as r:
        return r.read()


README = read_file("README.rst")
CONTRIB = read_file("CONTRIBUTING.rst")
CHANGES = read_file("CHANGES.rst")
version = read_file("VERSION.txt").strip()
test_deps = [
    "mock",
    "pytest>=3.1",
    "pytest-cov"
]

install_deps = ["luma.core>=0.9.5"]
if os.uname()[4].startswith("arm"):
    install_deps += "rpi-ws281x"

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
    install_requires=install_deps,
    setup_requires=pytest_runner,
    tests_require=["mock", "pytest", "pytest-cov"],
    extras_require={
        'docs': [
            'sphinx >= 1.5.1'
        ],
        'qa': [
            'rstcheck',
            'flake8'
        ],
        'test': test_deps
    },
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
