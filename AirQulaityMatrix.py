import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio

import adafruit_ahtx0
import adafruit_sgp30

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

ahtx0 = adafruit_ahtx0.AHTx0(i2c)
sgp30 = adafruit_sgp30
