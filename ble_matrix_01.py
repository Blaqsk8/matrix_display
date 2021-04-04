import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
 
from adafruit_airlift.esp32 import ESP32

# --- User Config --- #
# Static Display Text
HEADER_TEXT = " "
HEADER_LENGTH = len(HEADER_TEXT)*6

SALES_FEED = "sign-quotes.salestext"
QUOTES_FEED = "sign-quotes.signtext"
COLORS_FEED = "sign-quotes.signcolor"
SCROLL_DELAY = 0.04
UPDATE_DELAY = 600
# -------------------------#

# --- Display Release ---
displayio.release_displays()

# --- BLE Setup ---
esp32 = ESP32() # DEFAULT
adapter = esp32.start_bluetooth()
ble = BLERadio(adapter)
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

# --- Display Setup ---
displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=64, bit_depth=4,
    rgb_pins=[
        board.MTX_R1,
        board.MTX_G1,
        board.MTX_B1,
        board.MTX_R2,
        board.MTX_G2,
        board.MTX_B2
    ],
    addr_pins=[
        board.MTX_ADDRA,
        board.MTX_ADDRB,
        board.MTX_ADDRC,
        board.MTX_ADDRD
    ],
    clock_pin=board.MTX_CLK,
    latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE
)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=False)
# --------------------------------------------------------------- #

line1 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=0xff0000,
    text="This scroller is brought to you by CircuitPython RGBMatrix")
line1.x = display.width
line1.y = 8
 
line2 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=0x0080ff,
    text="Hello to all CircuitPython contributors worldwide <3")
line2.x = display.width
line2.y = 24
 
# Put each line of text into a Group, then show that group.
g = displayio.Group()
g.append(line1)
g.append(line2)
display.show(g)
 
# This function will scoot one label a pixel to the left and send it back to
# the far right if it's gone all the way off screen. This goes in a function
# because we'll do exactly the same thing with line1 and line2 below.
def scroll(line):
    line.x = line.x - 1
    line_width = line.bounding_box[2]
    if line.x < -line_width:
        line.x = display.width
 
# This function scrolls lines backwards.  Try switching which function is
# called for line2 below!
def reverse_scroll(line):
    line.x = line.x + 1
    line_width = line.bounding_box[2]
    if line.x >= display.width:
        line.x = -line_width
        
def update_text(text):
    line1.text = text
 
# You can add more effects in this loop. For instance, maybe you want to set the
# color of each label to a different value.
while True:
    ble.start_advertising(advertisement)
    print("waiting to connect")
    while not ble.connected:
        pass
    print("connected: trying to read input")
    while ble.connected:
        # Returns b'' if nothing was read.
        one_byte = uart.read(1)
        if one_byte:
            print(one_byte)
            ht = one_byte.decode()
            uart.write(one_byte)
            HEADER_TEXT += ht
            print(HEADER_TEXT)
        update_text(HEADER_TEXT)
    display.refresh(minimum_frames_per_second=0)
