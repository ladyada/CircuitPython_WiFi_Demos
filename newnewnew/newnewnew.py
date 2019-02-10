import time
import board
from digitalio import DigitalInOut, Direction
import adafruit_pyportal

# Get wifi details and more from a settings.py file
try:
    from settings import settings
except ImportError:
    print("WiFi settings are kept in settings.py, please add them there!")
    raise

# Set up where we'll be fetching data from
"""
DATA_SOURCE = "https://www.adafruit.com/api/product/4089"
IMAGE_LOCATION = ["product_image"]
NAME_LOCATION = ["product_name"]
URL_LOCATION = ["product_url"]
"""

DATA_SOURCE = "https://www.adafruit.com/api/products?format=micro&featured=1&random=1"
IMAGE_LOCATION = [0, "image"]
NAME_LOCATION = [0, "name"]
URL_LOCATION = [0, "url"]

cwd = __file__.rsplit('/', 1)[0]
pyportal = adafruit_pyportal.PyPortal(url=DATA_SOURCE,
                                      json_path=(NAME_LOCATION, URL_LOCATION),
                                      status_neopixel=board.NEOPIXEL,
                                      default_bg=cwd+"/new_background.bmp",
                                      text_font="/fonts/Arial.bdf",
                                      text_position=((5, 10), (5, 200)),
                                      text_color=(0xFFFFFF, 0xFFFFFF),
                                      text_wrap=(50, 50), # characters to wrap
                                      image_json_path=IMAGE_LOCATION,
                                      image_resize=(320,240),
                                      image_position=(0,0),
                                      debug=True)

while True:
    response = None
    try:
        response = pyportal.fetch()
        print("Response is", response)
    except RuntimeError as e:
        print("Some error occured, retrying! -", e)

    stamp = time.monotonic()
    while (time.monotonic() - stamp) < 20:
        if pyportal.ts.touch_point:
            pyportal.show_QR(bytes(response[1], 'utf-8'),
                             qr_size=128, position=(190,56))
    print("Hide QR")
    pyportal.show_QR(None)
