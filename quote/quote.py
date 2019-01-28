import time
import board
import adafruit_pyportal
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.text_area import TextArea

# Set up where we'll be fetching data from
DATA_SOURCE = "https://www.adafruit.com/api/quotes.php"
DATA_LOCATION = [0]

pyportal = adafruit_pyportal.PyPortal(url=DATA_SOURCE, json_path=DATA_LOCATION,
                           backlight=board.TFT_BACKLIGHT, status_neopixel=board.NEOPIXEL,
                           default_bg="quote_background.bmp")

quote_font = bitmap_font.load_font("/fonts/Arial-ItalicMT-17.bdf")
quote_font.load_glyphs(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
quote_position = (10, 30)
quote_color = 0xFFFFFF
author_font = quote_font
author_position = (150, 180)
author_color = 0x0000FF

# return a list of lines with wordwrapping
def wrap_nicely(string, max_chars):
    words = string.split(' ')
    the_lines = []
    the_line = ""
    for w in words:
        if len(the_line+' '+w) <= max_chars:
            the_line += ' '+w
        else:
            the_lines.append(the_line)
            the_line = ''+w
    if the_line:      # last line remaining
        the_lines.append(the_line)
    return the_lines

value = {'text': 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industrys standard', 'author': 'Harriet Tubman'}
quote_text = None
author_text = None
def draw_text(quote, author):
    global quote_text, author_text
    if quote_text:
        pyportal.splash.pop()
    if author_text:
        pyportal.splash.pop()
    quote = '\n'.join(wrap_nicely(quote, 38))
    quote_text = TextArea(quote_font, text=quote)
    quote_text.color = quote_color
    quote_text.x = quote_position[0]
    quote_text.y = quote_position[1]
    pyportal.splash.append(quote_text.group)

    author_text = TextArea(author_font, text=author)
    author_text.color = author_color
    author_text.x = author_position[0]
    author_text.y = author_position[1]
    pyportal.splash.append(author_text.group)

    board.DISPLAY.wait_for_frame()

draw_text(value['text'], value['author'])

while True:
    try:
        value = pyportal.fetch()
        print("Response is", value)
        draw_text(value['text'], value['author'])
    except RuntimeError as e:
        print("Some error occured, retrying! -", e)
        pyportal._esp.debug=True
    time.sleep(5)
