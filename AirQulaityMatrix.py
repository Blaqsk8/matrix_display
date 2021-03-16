import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import time
import terminalio

import adafruit_ahtx0
import adafruit_sgp30

i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)

# Release any other displays so we can create our own
displayio.release_displays()

# Create all my hardware objects
ahtx0 = adafruit_ahtx0.Adafruit_AHTX0(i2c)
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
matrix = rgbmatrix.RGBMatrix(
    width=32, height=32, bit_depth=1,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

# Initialize and get MOX baseline readings
sgp30.iaq_init()
sgp.set_iaq_baseline(0x8973, 0x8AAE)

# Associate RGB matrix with a Display as to use displayio features
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)

group = displayio.Group()



# Start an infinite loop in order to get sensor data and display on matrix
while True:
    # Get sensor data
    temperature_f = (ahtx0.temperature * 1.8) + 32
    humidity = ahtx0.relative_humidity
    eCO2 = sgp30.eC02
    tvoc = sgp30.TVOC
    # Get all the data formatted for display
    text_temp = str(temperature_f)
    text_hum = str(humidity)
    text_CO2 = str(eCO2)
    text_TVOC = str(tvoc)
    # Wait 1 second to get sensor data
    time.sleep(1)
    
    
    
