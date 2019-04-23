# -*- coding: utf-8 -*-
# Copyright (c) 2019 Juan Antonio Martinez <jonsito at gmail dot com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
# OR OTHER DEALINGS IN THE SOFTWARE.

import atexit
import json
import sys
import time
import spidev
import threading

import RPi.GPIO as GPIO
#import GPIOEmu as GPIO

from luma.core.device import device
import luma.core.const
from luma.core.interface.serial import noop

# HUB08 connector pinout
#
# GND *  * addr-A
# GND *  * addr-B
# GND *  * addr-C
#  EN *  * addr-D
#  R1 *  * G1
#  R2 *  * G2
# GND *  * Latch
# GND *  * Clock

# Hub08 pin assignments ( shift-register related )
spi_clock = 23 # GPIO 11 / SPI0_CLK / HUB08_CLOCK
spi_dout = 19 # GPIO 10 / SPI0_DATA_OUT / HUB08_R1
spi_din = 21 # GPIO 09 / SPI0_DATA_IN --- NOT USED
spi_cs = 24 # GPIO 08 / SPI0_CE_0 --- NOT USED
red2 = 7 # GPIO 07 / HUB08 R2

# HUB08 pin assignment ( row addressing and data transfer )
latch = 22 # GPIO 25
enable = 18 # GPIO 24
addr0 = 16 # GPIO 23
addr1 = 11 # GPIO 17
addr2 = 13 # GPIO 27
addr3 = 15 # GPIO 22

# table to linearize bright values for setting pwm duty cycle
# from https://forum.arduino.cc/index.php?topic=96839.0
brightness_table= [
	0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
	0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,
	1,  1,  1,  1,  1,  1,  1,  1,  1,  2,  2,  2,  2,  2,  2,  2,
	2,  3,  3,  3,  3,  3,  3,  3,  4,  4,  4,  4,  4,  5,  5,  5,
	5,  6,  6,  6,  6,  7,  7,  7,  7,  8,  8,  8,  9,  9,  9, 10,
	10, 10, 11, 11, 11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16,
	17, 17, 18, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23, 24, 24, 25,
	25, 26, 27, 27, 28, 29, 29, 30, 31, 32, 32, 33, 34, 35, 35, 36,
	37, 38, 39, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 50,
	51, 52, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 66, 67, 68,
	69, 70, 72, 73, 74, 75, 77, 78, 79, 81, 82, 83, 85, 86, 87, 89,
	90, 92, 93, 95, 96, 98, 99,101,102,104,105,107,109,110,112,114,
	115,117,119,120,122,124,126,127,129,131,133,135,137,138,140,142,
	144,146,148,150,152,154,156,158,160,162,164,167,169,171,173,175,
	177,180,182,184,186,189,191,193,196,198,200,203,205,208,210,213,
	215,218,220,223,225,228,231,233,236,239,241,244,247,249,252,255
]

class hub08(device):
	"""
	Implementation for HUB08 led display driver for luma.core.device

	.. note::
		Direct use of the :func:`command` and :func:`data` methods are
		discouraged: Screen updates should be effected through the
		:func:`display` method, or preferably with the
		:class:`luma.core.render.canvas` context manager.
	"""

	# variables
	state = False # true: refresh active, false: do not refresh
	brightness = 0  # 0: full brigthness .. 100: turn off
	refresh_period = 0.0001 # 0.1 mseg
	mode='1' # 1-color only
	width=64
	height=16
	rotate=0
	# use double-buffering
	active_buffer = 0
	display_data = [
		[#eigh bytes (64 pixels) on each row
			[255,0,0,0,0,0,0,0], # row 0
		 	[0,255,0,0,0,0,0,0], # row 1
		 	[0,0,255,0,0,0,0,0], # row 2
		 	[0,0,0,255,0,0,0,0], # row 3
		 	[0,0,0,0,255,0,0,0], # row 4
		 	[0,0,0,0,0,255,0,0], # row 5
		 	[0,0,0,0,0,0,255,0], # row 6
		 	[0,0,0,0,0,0,0,255], # row 7
		 	[0,0,0,0,0,0,0,255], # row 8
		 	[0,0,0,0,0,0,255,0], # row 9
		 	[0,0,0,0,0,255,0,0], # row 10
		 	[0,0,0,0,255,0,0,0], # row 11
		 	[0,0,0,255,0,0,0,0], # row 12
		 	[0,0,255,0,0,0,0,0], # row 13
		 	[0,255,0,0,0,0,0,0], # row 14
		 	[255,0,0,0,0,0,0,0], # row 15
		 	# next values are only used in 32 row led matrices
			[255,0,0,0,0,0,0,0], # row 16
		 	[0,255,0,0,0,0,0,0], # row 17
		 	[0,0,255,0,0,0,0,0], # row 18
		 	[0,0,0,255,0,0,0,0], # row 19
		 	[0,0,0,0,255,0,0,0], # row 20
		 	[0,0,0,0,0,255,0,0], # row 21
		 	[0,0,0,0,0,0,255,0], # row 22
		 	[0,0,0,0,0,0,0,255], # row 23
		 	[0,0,0,0,0,0,0,255], # row 24
		 	[0,0,0,0,0,0,255,0], # row 25
		 	[0,0,0,0,0,255,0,0], # row 26
		 	[0,0,0,0,255,0,0,0], # row 26
		 	[0,0,0,255,0,0,0,0], # row 28
		 	[0,0,255,0,0,0,0,0], # row 29
		 	[0,255,0,0,0,0,0,0], # row 30
		 	[255,0,0,0,0,0,0,0]  # row 31
		],
		[ #eigh bytes (64 pixels) on each row
			[255,0,0,0,0,0,0,0], # row 0
			[0,255,0,0,0,0,0,0], # row 1
			[0,0,255,0,0,0,0,0], # row 2
			[0,0,0,255,0,0,0,0], # row 3
			[0,0,0,0,255,0,0,0], # row 4
			[0,0,0,0,0,255,0,0], # row 5
			[0,0,0,0,0,0,255,0], # row 6
			[0,0,0,0,0,0,0,255], # row 7
			[0,0,0,0,0,0,0,255], # row 8
			[0,0,0,0,0,0,255,0], # row 9
			[0,0,0,0,0,255,0,0], # row 10
			[0,0,0,0,255,0,0,0], # row 11
			[0,0,0,255,0,0,0,0], # row 12
			[0,0,255,0,0,0,0,0], # row 13
			[0,255,0,0,0,0,0,0], # row 14
			[255,0,0,0,0,0,0,0], # row 15
		 	# next values are only used in 32 row led matrices
			[255,0,0,0,0,0,0,0], # row 16
		 	[0,255,0,0,0,0,0,0], # row 17
		 	[0,0,255,0,0,0,0,0], # row 18
		 	[0,0,0,255,0,0,0,0], # row 19
		 	[0,0,0,0,255,0,0,0], # row 20
		 	[0,0,0,0,0,255,0,0], # row 21
		 	[0,0,0,0,0,0,255,0], # row 22
		 	[0,0,0,0,0,0,0,255], # row 23
		 	[0,0,0,0,0,0,0,255], # row 24
		 	[0,0,0,0,0,0,255,0], # row 25
		 	[0,0,0,0,0,255,0,0], # row 26
		 	[0,0,0,0,255,0,0,0], # row 26
		 	[0,0,0,255,0,0,0,0], # row 28
		 	[0,0,255,0,0,0,0,0], # row 29
		 	[0,255,0,0,0,0,0,0], # row 30
		 	[255,0,0,0,0,0,0,0]  # row 31
		]
	]
	cur_row = 0 # row being serialized

	def refresh(self):
		while self.refresh_period >0: # loop until end of thread signaled
			if self.state == True:
				row=self.display_data[self.active_buffer][self.cur_row]
				row2=self.display_data[self.active_buffer][self.cur_row+16]
				self.enabled.ChangeDutyCycle(100) # turn off display ( set enable gpio high )
				for i in range(8):
					byte=row[i]
					byte2=row2[i]
					for bit in range(8):
						val = (byte & (1<<bit)) != 0
						val2 = (byte2 & (1<<bit)) != 0
						GPIO.output(spi_dout,val) # HUB08 R1 data
						GPIO.output(red2,val2) # HUB08 R2 data
						GPIO.output(spi_clock,False)
						GPIO.output(spi_clock,True) # clock tick to shift-register

				#transfer row data using SPI
				# self.spi.writebytes(row)
				# store sent data into current row
				GPIO.output(addr0, (self.cur_row & 0x01)!=0 )
				GPIO.output(addr1, (self.cur_row & 0x02)!=0 )
				GPIO.output(addr2, (self.cur_row & 0x04)!=0 )
				GPIO.output(addr3, (self.cur_row & 0x08)!=0 ) # select row (0..15 for R1, 16..31 for R2)
				GPIO.output(latch,False)
				GPIO.output(latch,True) # latch data from shift register to drive leds
				self.enabled.ChangeDutyCycle(self.brightness) # re-enable display
				# and finally increase cursor
				# notice that cursor range is 0..15 as rows 16..31 are processed together
				self.cur_row = (self.cur_row + 1 ) & 0x0F
			time.sleep(self.refresh_period)

	def initialize(self):
		self.state = False
		# Setup breakout board
		GPIO.setmode(GPIO.BOARD) # number pins according board pin number ( alternative to GPIO.BCM )

		# gpios related to transfer data
		# this code should rewritten to use SPI, but in gpio mode works fine
		GPIO.setup(spi_clock,GPIO.OUT)
		GPIO.setup(spi_dout,GPIO.OUT)
		GPIO.setup(spi_din,GPIO.IN)
		GPIO.setup(spi_cs,GPIO.OUT)
		GPIO.setup(red2,GPIO.OUT)
		GPIO.output(spi_clock, True) # default high
		GPIO.output(spi_dout, True)
		GPIO.output(red2, True)
		GPIO.output(spi_cs, False) # default low (enabled)

		# SPI related code disabled cause no easy way to handle 2 simultaneous SPI channels
		#self.spi = spidev.SpiDev()
		#self.spi.open(0, 0)
		#self.spi.no_cs = True
		#self.spi.threewire = False
		#self.spi.bits_per_word = 8
		#self.spi.mode = 0b00
		#self.spi.max_speed_hz = 100000

		# use enable pin as PWM, to allow set brightness
		# remember enable pin is active low
		GPIO.setup(enable,GPIO.OUT)
		self.enabled = GPIO.PWM(enable, 100000) # set 100KHz as frecuency
		self.enabled.start(50) # default is 50% duty cycle

		#GPIOs
		GPIO.setup(latch,GPIO.OUT)
		GPIO.setup(addr0,GPIO.OUT)
		GPIO.setup(addr1,GPIO.OUT)
		GPIO.setup(addr2,GPIO.OUT)
		GPIO.setup(addr3,GPIO.OUT)
		GPIO.output(latch, True) # turn off (negative logic)
		GPIO.output(addr0, False) # default 0
		GPIO.output(addr1, False) # default 0
		GPIO.output(addr2, False) # default 0
		GPIO.output(addr3, False) # default 0

		# GPS module ( RX-TX)

	def __init__(self,width=64, height=16, rotate=0, mode="1"):
		super(hub08, self).__init__(const=None,serial_interface=noop)
		self.capabilities(width, height, rotate,mode)
		self.image = None
		self.size=(width,height)
		self.refresh_period=0.0001 # 0.1 msecs between consecutive rows refresh
		self.initialize()
		self.refresh_thread = threading.Thread(target = self.refresh) # led matrix refresh thread loop
		self.refresh_thread.start()
		def shutdown_hook():  # pragma: no cover
			self.state=False # disable refresh
			self.refresh_period = -1 # tell refresh thread to exit
			try:
				GPIO.cleanup()
				self.cleanup()
			except:
				pass
		atexit.register(shutdown_hook)

	# at this momment onlu 64x16, no rotate, and single color is supported
	def capabilities(self,width, height, rotate, mode='1'):
		assert(width == 64)
		assert( (height==16) or (height==32) )
		assert(rotate == 0) # no rotation (yet)
		assert(mode == '1') # luma modes are "1", "rgb" and "rgba"
		self.width=width
		self.height=height
		self.rotate=rotate
		self.mode=mode

	def display(self,image):
		# create a bitmap from provided pixelmap, to be sent to display by mean of refresh trhead
		assert(image.mode == self.mode)
		assert(image.size == self.size)
		if self.state == False:
			return
		im = super(hub08, self).preprocess(image)
		pixels=list(im.getdata())
		width, height = im.size
		# use non active buffer to populate data
		idx= self.active_buffer^0x01
		# iterate over 16 rows
		for row in range(self.height): # 16/32 rows
			# send 64 bits to shift-register
			for column in range(self.width): # 64 columns
				byte = column>>3 # 8 bits per byte
				mask  = 0x01 << int(column&0x07)
				pixel= pixels[self.width*row + column]
				# 0 is black 255:white... but matrix reverse colors
				if pixel == 0:
					cur = self.display_data[idx][row][byte] | mask
				else:
					cur = self.display_data[idx][row][byte] & ~mask
				self.display_data[idx][row][byte] = cur
		# make this buffer active
		self.active_buffer = self.active_buffer^0x01

	def show(self):
		"""
		Sets the display mode ON, waking the device out of a prior
		low-power sleep mode.
		"""
		self.enabled.ChangeDutyCycle(self.brightness)
		self.state=True

	def hide(self):
		"""
		Switches the display mode OFF, putting the device in low-power
		sleep mode.
		led matrix "enable" pin has negative logic so set pwm to 100% makes display turn off
		"""
		self.enabled.ChangeDutyCycle(100)
		self.state=False

	def contrast(self, level):
		"""
		Switches the display contrast to the desired level, in the range
		0-255. Note that setting the level to a low (or zero) value will
		not necessarily dim the display to nearly off. In other words,
		this method is **NOT** suitable for fade-in/out animation.

		hub08 display has no way to set up bright. The only way to handle this
		is by mean of using enable pin as PWM, and changeing duty cycle

		:param level: Desired contrast level in the range of 0-255.
		:type level: int
		"""
		assert(0 <= level <= 255)
		lvl = brightness_table[255-level] # human vision is nonlinear: use lookup table
		self.brightness = int( (lvl*100)/255)

	def cleanup(self):
		"""
		Attempt to switch the device off or put into low power mode (this
		helps prolong the life of the device), clear the screen and close
		resources associated with the underlying serial interface.

		If :py:attr:`persist` is True, the device will not be switched off.

		This is a managed function, which is called when the python processs
		is being shutdown, so shouldn't usually need be called directly in
		application code.
		"""
		if not self.persist:
			self.hide()
			self.clear()
			self.period=-1
		self._serial_interface.cleanup()
