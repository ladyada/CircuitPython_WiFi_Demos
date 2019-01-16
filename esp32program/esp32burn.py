import time
import board
import busio
import microcontroller

from digitalio import DigitalInOut, Direction # pylint: disable=unused-import
from Adafruit_CircuitPython_miniesptool import adafruit_miniesptool

print("ESP32 mini prog")

# Py portal
uart = busio.UART(board.TX, board.RX, timeout=1)
resetpin = DigitalInOut(board.ESP_RESET)
gpio0pin = DigitalInOut(board.ESP_GPIO0)
esptool = adafruit_miniesptool.miniesptool(uart, gpio0pin, resetpin,
                                           flashsize=4*1024*1024)
esptool.debug = False

for i in range(5):
    try:
        esptool.sync()
        break
    except RuntimeError:
        pass
print("Synced")
print("Found:", esptool.chip_name)
if esptool.chip_name != "ESP32":
    raise RuntimeError("This example is for ESP32 only")
esptool.baudrate = 921600
print("MAC ADDR: ", [hex(i) for i in esptool.mac_addr])

# 0x10000 ota_data_initial.bin
esptool.flash_file("esp32/ota_data_initial.bin", 0x10000,
                   '84d04c9d6cc8ef35bf825d51a5277699')

# 0x1000 bootloader/bootloader.bin
esptool.flash_file("esp32/bootloader/bootloader.bin", 0x1000,
                   'cfa1fa197de3fd117f857eedb10797d0')

# 0x20000 at_customize.bin
esptool.flash_file("esp32/at_customize.bin", 0x20000,
                   '9853055e077ba0c90cd70691b9d8c3d5')

# 0x24000 customized_partitions/server_cert.bin
esptool.flash_file("esp32/customized_partitions/server_cert.bin", 0x24000,
                   '766fa1e87aabb9ab78ff4023f6feb4d3')

# 0x26000 customized_partitions/server_key.bin
esptool.flash_file("esp32/customized_partitions/server_key.bin", 0x26000,
                   '05da7907776c3d5160f26bf870592459')

# 0x28000 customized_partitions/server_ca.bin
esptool.flash_file("esp32/customized_partitions/server_ca.bin", 0x28000,
                   'e0169f36f9cb09c6705343792d353c0a')

# 0x2a000 customized_partitions/client_cert.bin
esptool.flash_file("esp32/customized_partitions/client_cert.bin", 0x2a000,
                   '428ed3bae5d58b721b8254cbeb8004ff')

# 0x2c000 customized_partitions/client_key.bin
esptool.flash_file("esp32/customized_partitions/client_key.bin", 0x2c000,
                   '136f563811930a5d3bf04c946f430ced')

# 0x2e000 customized_partitions/client_ca.bin
esptool.flash_file("esp32/customized_partitions/client_ca.bin", 0x2e000,
                   '25ab638695819daae67bcd8a4bfc5626')

#  0xf000 phy_init_data.bin
esptool.flash_file("esp32/phy_init_data.bin", 0xf000,
                   'bc9854aa3687ca73e25d213d20113b23')

# 0x100000 esp-at.bin
esptool.flash_file("esp32/esp-at.bin", 0x100000,
                   '144c4cd6bc063be4cfa5cb034ab91697')

# 0x8000 partitions_at.bin
esptool.flash_file("esp32/partitions_at.bin", 0x8000,
                   'd3d1508993d61aedf17280140fc22a6b')

esptool.reset()
time.sleep(0.5)
