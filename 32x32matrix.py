import adafruit_display_text.label
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import time

#----------| User Config |----------
line_1_list = ['ONLY', 'STOP']
line_2_list = ['WE', 'THE']
line_3_list = ['CAN', 'HATE']
REFRESH_RATE = 4
#-----------------------------------

# If there was a display before (protomatter, LCD, or E-paper), release it so
# we can create ours
displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=32, height=32, bit_depth=6,
    rgb_pins=[board.D6, board.D5, board.D9, board.D11, board.D10, board.D12],
    addr_pins=[board.A5, board.A4, board.A3, board.A2],
    clock_pin=board.D13, latch_pin=board.D0, output_enable_pin=board.D1)

# Associate the RGB matrix with a Display so that we can use displayio features
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)


line1 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=0xff0000,
    text="   ")
line1.x = 6
line1.y = 5

line2 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=0x7fff00,
    text="   ")
line2.x = 6
line2.y = 15

line3 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=0xff0000,
    text="   ")
line3.x = 6
line3.y = 25

# Put each line of text into a Group, then show that group.
g = displayio.Group()
g.append(line1)
g.append(line2)
g.append(line3)
display.show(g)

# This function cycles through a list to show different words
def change_text(line):
    
    for i in range(len(line_1_list)):
        if i == 0:
            line1.color = 0x673ab7
            line1.x = 4
            line2.color = 0xff0000
            line2.x = 10
            line3.color = 0xffffff
            line3.x = 7
        else:
            line1.color = 0xff0000
            line1.x = 5
            line2.color = 0x7fff00
            line2.x = 6
            line3.color = 0x42a5f5
            line3.x = 4
        print(line_1_list[i])
        line1.text = line_1_list[i]
        print(line_2_list[i])
        line2.text = line_2_list[i]
        print(line_3_list[i])
        line3.text = line_3_list[i]
        time.sleep(REFRESH_RATE)

while True:
    change_text(line1)
    change_text(line2)
    change_text(line3)
