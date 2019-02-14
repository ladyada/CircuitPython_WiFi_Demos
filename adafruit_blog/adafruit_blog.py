import time
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
CATEGORY="9995" # CircuitPython
POSTS_API_BASE="https://blog.adafruit.com/wp-json/wp/v2/posts"
POSTS_API_OPTIONS="?_fields=_links,title,link&_embed=1&context=embed&per_page=1&orderby=rand"
DATA_SOURCE = POSTS_API_BASE+POSTS_API_OPTIONS+"&categories=" + CATEGORY
IMAGE_LOCATION = [0, "_embedded", "wp:featuredmedia", 0, "source_url"]
TITLE_LOCATION = [0, "title", "rendered"]
URL_LOCATION = [0, "link"]

cwd = __file__.rsplit('/', 1)[0]
pyportal = adafruit_pyportal.PyPortal(url=DATA_SOURCE,
                                      json_path=(TITLE_LOCATION, URL_LOCATION),
                                      image_json_path=IMAGE_LOCATION,
                                      status_neopixel=board.NEOPIXEL,
                                      default_bg=cwd+"/adafruit_blog_background.bmp",
                                      text_font="/fonts/Arial.bdf",
                                      text_position=((5, 10), (5, 200)),
                                      text_color=(0xFFFFFF, 0xFFFFFF),
                                      text_maxlen=(50, 50, None), # cut off characters
                                      debug=False)

while True:
    response = None
    try:
        pyportal.set_background(None)
        response = pyportal.fetch()
        print("Response is", response)


    except RuntimeError as e:
        print("Some error occured, retrying! -", e)

    time.sleep(30)