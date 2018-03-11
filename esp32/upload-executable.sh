#!/bin/sh
python serial-uploader/esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 921600 \
  --before default_reset --after hard_reset write_flash -z --flash_mode dio \
  --flash_freq 80m --flash_size detect \
  0xe000  boot/boot_app0.bin \
  0x1000  boot/bootloader_dio_80m.bin \
  0x10000 websvf_sd/websvf_sd.ino.bin \
  0x8000  websvf_sd/websvf_sd.ino.partitions.bin 
