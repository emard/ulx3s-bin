#!/bin/sh -e

python ../serial-uploader/esptool.py --port /dev/ttyUSB0 --baud 460800 erase_flash

python ../serial-uploader/esptool.py --port /dev/ttyUSB0 \
  --baud 460800 write_flash -z 0x1000 \
  micropython/esp32-idf3-20191117-v1.11-580-g973f68780.bin
