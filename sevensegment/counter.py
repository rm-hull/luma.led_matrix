#!/usr/bin/env python2

from time import sleep

from sevenSegment import SevenSegment

segment = SevenSegment()

# tests overflow
segment.writeInt(99999999 + 1)
sleep(1)
# tests digit deletion, unused digits should be blanked
segment.writeInt(1234)
sleep(1)

# counting fast
count = 1;
while True:
   segment.writeInt(count)
   sleep(.05)
   count += 1

