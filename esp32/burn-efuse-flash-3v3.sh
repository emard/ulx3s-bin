#!/bin/sh
python serial-uploader/espefuse.py --port /dev/ttyUSB0 \
 set_flash_voltage 3.3V
