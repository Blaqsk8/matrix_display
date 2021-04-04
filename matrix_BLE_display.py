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
HEADER_TEXT = "Team P NSR"
HEADER_LENGTH = len(HEADER_TEXT)*6

SALES_FEED = "sign-quotes.salestext"
QUOTES_FEED = "sign-quotes.signtext"
COLORS_FEED = "sign-quotes.signcolor"
SCROLL_DELAY = 0.04
UPDATE_DELAY = 600
# -------------------------#

displayio.release_displays()

# If you are using a Metro M4 Airlift Lite, PyPortal,
# or MatrixPortal, you can use the default pin settings.
# Leave this DEFAULT line uncommented.
esp32 = ESP32() # DEFAULT

# --- Display setup ---


# Header Text (ID - 0)


adapter = esp32.start_bluetooth()
 
ble = BLERadio(adapter)
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

HEADER_TEXT = " "
 
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
