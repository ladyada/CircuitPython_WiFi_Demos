"""
This example will access an API, grab a number like hackaday skulls, github
stars, price of bitcoin, twitter followers... and display it on a screen if you can find something that
spits out JSON data, we can display it!
"""
import os
import gc
import time
import board
import busio
import microcontroller
from digitalio import DigitalInOut, Direction
import adafruit_espatcontrol
import adafruit_espatcontrol_requests as requests
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.text_area import TextArea
import ujson
import neopixel
import displayio
import pulseio

backlight = pulseio.PWMOut(board.TFT_BACKLIGHT)

splash = displayio.Group()
board.DISPLAY.show(splash)

# open background file and show it
cwd = __file__.rsplit('/', 1)[0]
f = open(cwd+"/background.bmp", "rb")
background = displayio.OnDiskBitmap(f)
face = displayio.Sprite(background, pixel_shader=displayio.ColorConverter(), position=(0,0))
splash.append(face)
board.DISPLAY.wait_for_frame()

# turn on backlight
backlight.duty_cycle = 2**15

# load font
font = bitmap_font.load_font(cwd+"/fonts/Checkbook-25.bdf")
text = None

def set_message(string):
    global text
    if text:
        splash.pop()
    text = TextArea(font, text=string)
    text.y = 100
    text.x = 180
    splash.append(text.group)
    board.DISPLAY.wait_for_frame()
    gc.collect()

set_message("SKULL VIEW!")

# Get wifi details and more from a settings.py file
try:
    from settings import settings
except ImportError:
    print("WiFi settings are kept in settings.py, please add them there!")
    raise

set_message("SETTINGS OK")

#              CONFIGURATION
PLAY_SOUND_ON_CHANGE = True
NEOPIXELS_ON_CHANGE = False
TIME_BETWEEN_QUERY = 15  # in seconds

# Some data sources and JSON locations to try out
DATA_SOURCE = "https://api.hackaday.io/v1/projects/163309?api_key="+settings['hackaday_token']
DATA_LOCATION = ["skulls"]

set_message("INIT ESP32")

uart = busio.UART(board.TX, board.RX, timeout=0.1)
resetpin = DigitalInOut(board.ESP_RESET)
rtspin = DigitalInOut(board.ESP_RTS)

# Create the connection to the co-processor and reset
esp = adafruit_espatcontrol.ESP_ATcontrol(uart, 115200, run_baudrate=921600,
                                          reset_pin=resetpin,
                                          rts_pin=rtspin, debug=True)
esp.hard_reset()

requests.set_interface(esp)

status = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)

# neopixels
if NEOPIXELS_ON_CHANGE:
    pixels = neopixel.NeoPixel(board.A1, 16, brightness=0.4, pixel_order=(1, 0, 2, 3))
    pixels.fill(0)

# music!
if PLAY_SOUND_ON_CHANGE:
    import audioio
    wave_file = open(cwd+"/coin.wav", "rb")
    wave = audioio.WaveFile(wave_file)

# we'll save the value in question
last_value = value = 0
the_time = None
times = 0

def chime_light():
    """Light up LEDs and play a tune"""
    if NEOPIXELS_ON_CHANGE:
        for i in range(0, 100, 10):
            pixels.fill((i, i, i))
    starpin.value = True

    if PLAY_SOUND_ON_CHANGE:
        with audioio.AudioOut(board.A0) as audio:
            audio.play(wave)
            while audio.playing:
                pass
    starpin.value = False

    if NEOPIXELS_ON_CHANGE:
        for i in range(100, 0, -10):
            pixels.fill((i, i, i))
        pixels.fill(0)

def get_value(response, location):
    """Extract a value from a json object, based on the path in 'location'"""
    try:
        print("Parsing JSON response...", end='')
        json = ujson.loads(response)
        print("parsed OK!")
        for x in location:
            json = json[x]
        return json
    except ValueError:
        print("Failed to parse json, retrying")
        return None

while True:
    try:
        status[0] = (0,0,100)
        while not esp.is_connected:
            # settings dictionary must contain 'ssid' and 'password' at a minimum
            set_message("ESP32 CONNECTING...")
            status[0] = (100, 0, 0) # red = not connected
            esp.connect(settings)
            set_message("ESP32 CONNECTED!")
        # great, lets get the data
        # get the time
        #the_time = esp.sntp_time

        print("Retrieving data source...", end='')
        status[0] = (100, 100, 0)   # yellow = fetching data
        r = requests.get(DATA_SOURCE)
        status[0] = (0, 0, 100)   # green = got data
        print("Reply is OK!")
    except (RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to get data, retrying\n", e)
        continue
    print('-'*40,)
    print("Headers: ", r.headers)
    print("Text:", r.text)
    print('-'*40)

    value = r.json()
    for x in DATA_LOCATION:
        value = value[x]
    if not value:
        continue

    print(times, the_time, "value:", value)
    set_message("SKULLS: %d" % value)
    times += 1

    # normally we wouldn't have to do this, but we get bad fragments
    r = value = None
    gc.collect()
    print(gc.mem_free())  # pylint: disable=no-member
    time.sleep(TIME_BETWEEN_QUERY)
