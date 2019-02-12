import time
import gc
import os
import random
import board
import adafruit_pyportal

# Get wifi details and more from a settings.py file
try:
    from settings import settings
except ImportError:
    print("WiFi settings are kept in settings.py, please add them there!")
    raise


# Set up where we'll be fetching data from
TWITTER_USER = "DuneQuoteBot"
TWITTER_TO_XML = "https://twitrss.me/twitter_user_to_rss/?user="
XML_TO_JSON = "http://www.unmung.com/mf2?url=http://www.unmung.com/feed?feed="
NUM_TWEETS=20  # how many tweets we get within a query to randomize from
DATA_SOURCE = XML_TO_JSON+TWITTER_TO_XML+TWITTER_USER
TEXT_LOCATION = ["items", 0, "children", 0, "properties", "name", 0]

cwd = __file__.rsplit('/', 1)[0]

# Find all image files on the storage
imagefiles = [file for file in os.listdir(cwd+"/backgrounds/")
             if (file.endswith(".bmp") and not file.startswith("._"))]
for i, filename in enumerate(imagefiles):
    imagefiles[i] = cwd+"/backgrounds/"+filename
print("Image files found: ", imagefiles)

pyportal = adafruit_pyportal.PyPortal(url=DATA_SOURCE,
                                      json_path=TEXT_LOCATION,
                                      status_neopixel=board.NEOPIXEL,
                                      default_bg=imagefiles[0],
                                      text_font="/fonts/Helvetica-Oblique-17.bdf",
                                      text_position=(15, 20),
                                      text_color=0xFFFFFF,
                                      text_wrap=35, # character to wrap around
                                      text_maxlen=280, # cut off characters
                                      debug=False)
pyportal._text_font.load_glyphs(b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.,! \'"')


while True:
    response = None
    try:
        pyportal.set_background(random.choice(imagefiles))
        response = pyportal.fetch()
        print("Response is", response)
    except (IndexError, RuntimeError, ValueError) as e:
        print("Some error occured, retrying! -", e)

    # next tweet should be random!
    tweet_idx = random.randint(0, NUM_TWEETS)
    TEXT_LOCATION[3] = tweet_idx
    gc.collect()
    time.sleep(10)
