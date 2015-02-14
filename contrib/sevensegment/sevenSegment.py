import max7219.led as led

# this is inspired by adafruits library
# https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code/tree/master/Adafruit_LEDBackpack


class SevenSegment:
  disp = None

  # Hexadecimal character lookup table (row 1 = 0..9, row 2 = A..F)
  digits = [ 0x7e, 0x30, 0x6d, 0x79, 0x33, 0x5b, 0x5f, 0x70, 0x7f, 0x7b, \
			0x77, 0x1f, 0x4e, 0x3d, 0x4f, 0x47 ]

  # Constructor
  def __init__(self, debug=False):
    #if (debug):
    #  print "Initializing a new instance of LEDBackpack at 0x%02X" % address
    self.disp = led
    self.disp.init()
    self.disp.clear()

  def writeDigitRaw(self, charNumber, value):
    "Sets a digit using the raw 16-bit value"
    if (charNumber > 8):
      return
    # Set the appropriate digit
    self.disp.send_byte(charNumber, value)

  def writeDigit(self, charNumber, value, dot=False):
    "Sets a single decimal or hexademical value (0..9 and A..F)"
    if (value > 0xF):
      return
    # Set the appropriate digit
    self.writeDigitRaw(charNumber, self.digits[value] | (dot << 7))

  def writeInt(self, d):
    digit = 1
    while (d > 0 and digit <= 8):
        v = d % 10;
        self.writeDigit(digit, v)
        digit += 1
        d = int(d / 10)
    while (digit <= 8):
        self.writeDigitRaw(digit, 0)
        digit += 1

