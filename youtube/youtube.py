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
CHANNEL_ID = "UCpOlOeQjj7EsVnDh3zuCgsA" # this isn't a secret but you have to look it up
DATA_SOURCE = "https://www.googleapis.com/youtube/v3/channels/?part=statistics&id="+CHANNEL_ID+"&key="+settings['youtube_token']
DATA_LOCATION1 = ["items", 0, "statistics", "viewCount"]
DATA_LOCATION2 = ["items", 0, "statistics", "subscriberCount"]

cwd = __file__.rsplit('/', 1)[0]
pyportal = adafruit_pyportal.PyPortal(url=DATA_SOURCE, json_path=(DATA_LOCATION1, DATA_LOCATION2),
                                      status_neopixel=board.NEOPIXEL,
                                      default_bg=cwd+"/youtube_background.bmp",
                                      text_font="/fonts/Collegiate-50.bdf",
                                      text_position=((100, 85), (180, 130)),
                                      text_color=(0xFFFFFF, 0xFFFFFF))

# track the last value so we can play a sound when it updates
last_subs = 0

while True:
    try:
        subs, views = pyportal.fetch()
        subs = int(subs)
        views = int(views)
        print("Response is", subs, views)
        if last_subs < subs:  # ooh it went up!
            print("New subscriber!")
            pyportal.play_file("coin.wav")
        last_subs = subs
    except RuntimeError as e:
        print("Some error occured, retrying! -", e)
    time.sleep(3)
