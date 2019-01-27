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
DATA_SOURCE = "https://api.github.com/repos/adafruit/circuitpython"
if 'github_token' in settings:
    DATA_SOURCE += "?access_token="+settings['github_token']
DATA_LOCATION = ["stargazers_count"]


pyportal = adafruit_pyportal.PyPortal(url=DATA_SOURCE, json_path=DATA_LOCATION,
                           backlight=board.TFT_BACKLIGHT, status_neopixel=board.NEOPIXEL,
                           default_bg="background.bmp",
                           text_font="/fonts/Collegiate-24.bdf",
                           text_position=(230, 75), text_color=0x000000)

# track the last value so we can play a sound when it updates
last_value = 0

while True:
    try:
        value = pyportal.fetch()
        print("Response is", value)
        if last_value < value:  # ooh it went up!
            print("New star!")
            pyportal.play_file("coin.wav")
        last_value = value
    except RuntimeError as e:
        print("Some error occured, retrying! -", e)
    time.sleep(3)
