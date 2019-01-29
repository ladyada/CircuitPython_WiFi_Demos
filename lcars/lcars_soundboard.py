import adafruit_touchscreen
import board
import displayio
import pulseio
import audioio
import time

IMAGE_FILE = "lcars.bmp"

# These pins are used as both analog and digital! XR and YU must be analog
# and digital capable. XL and YD just need to be digital
ts = adafruit_touchscreen.Touchscreen(board.TOUCH_XL, board.TOUCH_XR,
                                      board.TOUCH_YD, board.TOUCH_YU,
                                      calibration=((5200, 59000), (5800, 57000)),
                                      size=(320,240))

# Turn on backlight
backlight = pulseio.PWMOut(board.TFT_BACKLIGHT)

# define the bounding boxes for each button
red_button = ((25, 30), (65, 80))
yellow_button = ((25, 100), (65, 150))
blue_button = ((25, 170), (65, 230))
# and then make a list with all the button boxes and wave files
buttons = ((red_button, "red.wav"),
           (yellow_button, "yellow.wav"),
           (blue_button, "blue.wav"))

audio = audioio.AudioOut(board.AUDIO_OUT)
audiofilename = None
audiofile = None
def play_file(file_name):
    global audiofile, audiofilename
    print("Playing", file_name)
    if audio.playing: # stop previous audio file
        if audiofilename == file_name: # same file, bail!
            return
        audio.pause
        audiofile.close()
    # and play this file
    audiofile = open(file_name, "rb")
    audiofilename = file_name
    wavefile = audioio.WaveFile(audiofile)
    audio.play(wavefile)

# draw an image as a background
splash = displayio.Group()
background = displayio.OnDiskBitmap(open(IMAGE_FILE, "rb"))
bg_sprite = displayio.Sprite(background, pixel_shader=displayio.ColorConverter(), position=(0,0))
splash.append(bg_sprite)
board.DISPLAY.show(splash)
board.DISPLAY.wait_for_frame()

# turn on backlight
backlight.duty_cycle = 65535

while True:
    p = ts.touch_point
    if p:
        print(p)
        x, y, z = p
        for button in buttons:
            box = button[0]
            if (box[0][0] <= x <= box[1][0]) and (box[0][1] <= y <= box[1][1]):
                play_file(button[1])
    time.sleep(0.02)
