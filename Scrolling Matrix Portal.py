import time
import random
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal

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

# --- Display setup ---
matrixportal = MatrixPortal(status_neopixel=board.NEOPIXEL, debug=True)

# Scrolling Quote Text (ID - 0)
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(0, 25),
    scrolling=True,
)

# Static 'Connecting' Text (ID - 1)
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(2, 15),
)

# Static 'Team P NSR' Heading Text (ID - 2)
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=((matrixportal.graphics.display.width - HEADER_LENGTH) // 2, 3),
)

# Static Sales Text (ID - 3)
matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(5, 14),
)

sales = []
quotes = []
colors = []
last_sale = None
last_color = None
last_quote = None


def update_data():
    matrixportal.set_text(" ", 3)
    print("Updating data from Adafruit IO")
    matrixportal.set_text("Connecting", 1)

    try:
        sales_data = matrixportal.get_io_data(SALES_FEED)
        sales.clear()
        for json_data in sales_data:
            sales.append(matrixportal.network.json_traverse(json_data, ["value"]))
        print(sales)
    # pylint: disable=broad-except
    except Exception as error:
        print(error)

    try:
        quotes_data = matrixportal.get_io_data(QUOTES_FEED)
        quotes.clear()
        for json_data in quotes_data:
            quotes.append(matrixportal.network.json_traverse(json_data, ["value"]))
        print(quotes)
    # pylint: disable=broad-except
    except Exception as error:
        print(error)

    try:
        color_data = matrixportal.get_io_data(COLORS_FEED)
        colors.clear()
        for json_data in color_data:
            colors.append(matrixportal.network.json_traverse(json_data, ["value"]))
        print(colors)
    # pylint: disable=broad-except
    except Exception as error:
        print(error)

    if not quotes or not colors or not sales:
        raise RuntimeError("Please add at least one quote, sale, and color to your feeds")
    matrixportal.set_text(" ", 1)

update_data()
last_update = time.monotonic()
matrixportal.set_text(" ", 1)
sale_index = None
quote_index = None
color_index = None

while True:
    # Set the heading text
    matrixportal.set_text(HEADER_TEXT, 2)

    # Choose next Sale
    if len(sales) > 1 and last_sale is not None:

        while sale_index == last_sale:
            sale_index = random.randrange(0, len(sales))
    else:
        sale_index = random.randrange(0, len(sales))
    last_sale = sale_index

    # Choose a random quote from quotes
    if len(quotes) > 1 and last_quote is not None:
        while quote_index == last_quote:
            quote_index = random.randrange(0, len(quotes))
    else:
        quote_index = random.randrange(0, len(quotes))
    last_quote = quote_index

    # Choose a random color from colors
    if len(colors) > 1 and last_color is not None:
        while color_index == last_color:
            color_index = random.randrange(0, len(colors))
    else:
        color_index = random.randrange(0, len(colors))
    last_color = color_index

    # Set the sale text
    matrixportal.set_text(sales[sale_index], 3)
    

    # Set the quote text
    matrixportal.set_text(quotes[quote_index])

    # Set the text color
    matrixportal.set_text_color(colors[color_index])
    matrixportal.set_text_color(colors[color_index-1], 2)
    matrixportal.set_text_color(colors[color_index-2], 3)

    # Scroll it
    matrixportal.scroll_text(SCROLL_DELAY)

    if time.monotonic() > last_update + UPDATE_DELAY:
        update_data()
        last_update = time.monotonic()
