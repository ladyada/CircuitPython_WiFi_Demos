import time
import board
import adafruit_pyportal

# Set up where we'll be fetching data from
DATA_SOURCE = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
IMAGE_LOCATION = ["url"]
TITLE_LOCATION = ["title"]
DATE_LOCATION = ["date"]

cwd = __file__.rsplit('/', 1)[0]
pyportal = adafruit_pyportal.PyPortal(url=DATA_SOURCE,
                                      json_path=(TITLE_LOCATION, DATE_LOCATION),
                                      status_neopixel=board.NEOPIXEL,
                                      default_bg=cwd+"/nasa_background.bmp",
                                      text_font="/fonts/Arial.bdf",
                                      text_position=((5, 10), (5, 200)),
                                      text_color=(0xFFFFFF, 0xFFFFFF),
                                      text_maxlen=(50, 50), # cut off characters
                                      image_json_path=IMAGE_LOCATION,
                                      image_resize=(320, 240),
                                      image_position=(0, 0),
                                      debug=True)

while True:
    response = None
    try:
        response = pyportal.fetch()
        print("Response is", response)
    except RuntimeError as e:
        print("Some error occured, retrying! -", e)

    time.sleep(30*60)  # 30 minutes till next check
