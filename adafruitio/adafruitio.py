"""
This example will access an API, grab a number like hackaday skulls, github
stars, price of bitcoin, twitter followers... and display it on a screen if you can find something that
spits out JSON data, we can display it!
"""
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
DATA_SOURCE = "https://io.adafruit.com/api/v2/stats?x-aio-key="+settings['adafruitio_key']
DATA_LOCATION1 = ["io_plus", "io_plus_subscriptions"]
DATA_LOCATION2 = ["users", "users_active_30_days"]

cwd = __file__.rsplit('/', 1)[0]
pyportal = adafruit_pyportal.PyPortal(url=DATA_SOURCE,
                                      json_path=(DATA_LOCATION1, DATA_LOCATION2),
                                      status_neopixel=board.NEOPIXEL,
                                      default_bg=cwd+"/adafruitio_background.bmp",
                                      text_font="/fonts/Collegiate-24.bdf",
                                      text_position=((165, 145), (165, 178)),
                                      text_color=(0x00FF00, 0x0000FF))

# track the last value so we can play a sound when it updates
last_value = 0

while True:
    try:
        value = pyportal.fetch()
        print("Response is", value)
        last_value = value
    except RuntimeError as e:
        print("Some error occured, retrying! -", e)
    time.sleep(10)
