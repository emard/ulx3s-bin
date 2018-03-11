#!/bin/sh
python serial-uploader/esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 921600 \
  --before default_reset --after hard_reset write_flash -z --flash_mode dio \
  --flash_freq 80m --flash_size detect \
  0x00291000 websvf_sd/websvf_sd.spiffs.bin
