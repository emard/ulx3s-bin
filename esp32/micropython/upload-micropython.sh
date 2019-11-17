#!/bin/sh

ujprog ../../fpga/passthru/passthru-v20-12f/passthru_ulx3s_v20_12k.bit
ujprog ../../fpga/passthru/passthru-v20-25f/passthru_ulx3s_v20_25k.bit
ujprog ../../fpga/passthru/passthru-v20-45f/passthru_ulx3s_v20_45k.bit
ujprog ../../fpga/passthru/passthru-v20-85f/ulx3s_85f_passthru.bit

python ../serial-uploader/esptool.py --port /dev/ttyUSB0 --baud 460800 erase_flash

python ../serial-uploader/esptool.py --port /dev/ttyUSB0 \
  --baud 460800 write_flash -z 0x1000 \
  esp32-idf3-20191117-v1.11-580-g973f68780.bin
