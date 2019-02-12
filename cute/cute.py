import time
import board
import adafruit_pyportal

# Set up where we'll be fetching data from

# random cat
#DATA_SOURCE = "https://aws.random.cat/meow"
#IMAGE_LOCATION = ["file"]

# random fox
#DATA_SOURCE = "https://randomfox.ca/floof/"  # not working for some reason
#IMAGE_LOCATION = ["image"]

# random shibe
DATA_SOURCE = "http://shibe.online/api/shibes?count=1"
IMAGE_LOCATION = [0]

# more random cats!
#DATA_SOURCE = "https://api.thecatapi.com/v1/images/search"
#IMAGE_LOCATION = [0, "url"]

cwd = __file__.rsplit('/', 1)[0]
pyportal = adafruit_pyportal.PyPortal(url=DATA_SOURCE,
                                      status_neopixel=board.NEOPIXEL,
                                      default_bg=cwd+"/cute_background.bmp",
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

    time.sleep(10)  # 30 secs till next check
