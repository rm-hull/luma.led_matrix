#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
from io import open
from setuptools import setup


def read_file(fname, encoding='utf-8'):
    with open(fname, encoding=encoding) as r:
        return r.read()


def find_version(*file_paths):
    fpath = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = read_file(fpath)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)

    err_msg = 'Unable to find version string in {}'.format(fpath)
    raise RuntimeError(err_msg)


README = read_file('README.rst')
CONTRIB = read_file('CONTRIBUTING.rst')
CHANGES = read_file('CHANGES.rst')
version = find_version('luma', 'led_matrix', '__init__.py')

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []
test_deps = [
    'mock;python_version<"3.3"',
    'pytest>=3.1',
    'pytest-cov'
]

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
    install_requires=["luma.core>=1.2.1"],
    setup_requires=pytest_runner,
    tests_require=test_deps,
    extras_require={
        ':platform_machine=="armv7l" and platform_system=="Linux"': [
            'ws2812', 'rpi_ws281x'
        ],
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
        "Development Status :: 5 - Production/Stable",
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
