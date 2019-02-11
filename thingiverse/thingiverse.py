import time
import board
import adafruit_pyportal

# Get wifi details and more from a settings.py file
try:
    from settings import settings
except ImportError:
    print("WiFi settings are kept in settings.py, please add them there!")
    raise

# Set up where we'll be fetching data from
DATA_SOURCE = "https://api.thingiverse.com/users/adafruit/things?per_page=1&access_token=" + settings['thingiverse_token']
print(DATA_SOURCE)
IMAGE_LOCATION = [0, "thumbnail"]
TITLE_LOCATION = [0, "name"]
URL_LOCATION = [0, "url"]

cwd = __file__.rsplit('/', 1)[0]
pyportal = adafruit_pyportal.PyPortal(url=DATA_SOURCE,
                                      json_path=(TITLE_LOCATION, URL_LOCATION, IMAGE_LOCATION),
                                      status_neopixel=board.NEOPIXEL,
                                      default_bg=cwd+"/thingiverse_background.bmp",
                                      text_font="/fonts/Arial.bdf",
                                      text_position=((5, 10), (5, 200), None),
                                      text_color=(0xFFFFFF, 0xFFFFFF, None),
                                      text_maxlen=(50, 50, None), # cut off characters
                                      debug=True)

while True:
    response = None
    try:
        response = pyportal.fetch()
        print("Response is", response)
        image_url = response[2].replace('_thumb_medium.jpg', '_display_medium.jpg')
        pyportal.wget(adafruit_pyportal.IMAGE_CONVERTER_SERVICE+image_url, "/cache.bmp")
        pyportal.set_background("/cache.bmp")

    except RuntimeError as e:
        print("Some error occured, retrying! -", e)

    time.sleep(60)
