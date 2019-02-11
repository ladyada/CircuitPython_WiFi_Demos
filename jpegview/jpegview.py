import time
import board
import busio
from digitalio import DigitalInOut
import microcontroller
import adafruit_sdcard
import storage
import displayio
import pulseio
import os

from adafruit_esp32spi import adafruit_esp32spi
import adafruit_esp32spi.adafruit_esp32spi_requests as requests

print("ESP32 JPEG viewer")

SERVICE = "http://ec2-107-23-37-170.compute-1.amazonaws.com/rx/ofmt_bmp,rz_320x240/"
#SERVICE = "https://res.cloudinary.com/schmarty/image/fetch/w_320,h_240,c_fill,f_bmp/"
JPEGURL = "https://cdn-shop.adafruit.com/970x728/4089-03.jpg"
#"https://cdn-shop.adafruit.com/970x728/3900-07.jpg"
#JPEGURL = "https://cdn.thingiverse.com/renders/77/0c/f0/f6/2e/dbc6c3056540bdf03757ecc90fbe4b5f_preview_featured.jpg"

URL = SERVICE + JPEGURL

FILENAME = "/cache.bmp"

backlight = pulseio.PWMOut(board.TFT_BACKLIGHT)
backlight.duty_cycle = 30000

# Make ESP32 connection
esp32_cs = DigitalInOut(microcontroller.pin.PB14)
esp32_ready = DigitalInOut(microcontroller.pin.PB16)
esp32_gpio0 = DigitalInOut(microcontroller.pin.PB15)
esp32_reset = DigitalInOut(microcontroller.pin.PB17)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset, esp32_gpio0)
requests.set_interface(esp)
esp.connect_AP(b'adafruit', b'ffffffff')
print("Connected to", str(esp.ssid, 'utf-8'), "RSSI", esp.rssi)

print("Fetching stream from", URL)
r = requests.get(URL, stream=True)
#esp._debug = True

print(r.headers)
content_length = int(r.headers['content-length'])
remaining = content_length
print("Saving data to ", FILENAME)

stamp = time.monotonic()
with open(FILENAME, "wb") as f:
    for i in r.iter_content(min(remaining, 12000)):
        remaining -= len(i)
        f.write(i)
        print("Read %d bytes, %d remaining" % (content_length-remaining, remaining))
        if not remaining:
            break
r.close()
print(time.monotonic()-stamp, "seconds")
print(os.listdir("/"))
print("Created file of %d bytes" % os.stat(FILENAME)[6])

splash = displayio.Group()
board.DISPLAY.show(splash)
bg_file = open(FILENAME, "rb")
background = displayio.OnDiskBitmap(bg_file)
bg_sprite = displayio.Sprite(background, pixel_shader=displayio.ColorConverter(), position=(0,0))
splash.append(bg_sprite)
board.DISPLAY.wait_for_frame()

while True:
    pass
