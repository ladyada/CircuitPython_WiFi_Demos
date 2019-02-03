import time
import board
import busio
import microcontroller

from digitalio import DigitalInOut, Direction # pylint: disable=unused-import
from Adafruit_CircuitPython_miniesptool import adafruit_miniesptool

print("ESP32 mini prog")

# Py portal
uart = busio.UART(microcontroller.pin.PB12, microcontroller.pin.PB13, timeout=1)
resetpin = DigitalInOut(board.ESP_RESET)
gpio0pin = DigitalInOut(board.ESP_GPIO0)
ctspin = DigitalInOut(microcontroller.pin.PA12)
ctspin.direction = Direction.OUTPUT
ctspin.value = True
esptool = adafruit_miniesptool.miniesptool(uart, gpio0pin, resetpin,
                                           flashsize=4*1024*1024)
esptool.debug = False

esptool.sync()
print("Synced")
print("Found:", esptool.chip_name)
if esptool.chip_name != "ESP32":
    raise RuntimeError("This example is for ESP32 only")
esptool.baudrate = 921600
print("MAC ADDR: ", [hex(i) for i in esptool.mac_addr])

# combined firmware
cwd = __file__.rsplit('/', 1)[0]
esptool.flash_file(cwd+"/NINA_W102.bin", 0x0, '7353586e47d49505880d6d02740eb102')

esptool.reset()
time.sleep(0.5)
