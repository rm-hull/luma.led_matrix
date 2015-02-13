#!/usr/bin/env python2

from time import sleep
import sys

from sevenSegment import SevenSegment

segment = SevenSegment()

def _all():
 for x in range(256):
  print(x)
  segment.writeDigitRaw(1, x)
  sys.stdin.read(1)

def _hex():
 for x in range(16):
  segment.writeDigit(1, x)
  sleep(1)

def _affe():
 segment.writeDigit(8, 13)
 segment.writeDigit(7, 14)
 segment.writeDigit(6, 10)
 segment.writeDigit(5, 13)
 segment.writeDigit(4, 10)
 segment.writeDigit(3, 15)
 segment.writeDigit(2, 15)
 segment.writeDigit(1, 14)

#_all()
#_hex()
_affe()
