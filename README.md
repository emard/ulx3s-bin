# ULX3S binaries

A collection of functional binary files and uploaders
to quickstart with ULX3S. Works from Debian Linux.
Connect USB PC port with micro-USB cable to US1 port of ULX3S.
Green LED D18 should turn ON.

Set ftdi usbserial name

    usb-jtag/linux/ftx_prog --max-bus-power 500
    usb-jtag/linux/ftx_prog --manufacturer "FER-RADIONA-EMARD"
    usb-jtag/linux/ftx_prog --product "ULX3S FPGA 45K v1.7"

Re-plug USB, device will appear with above name.
Upload f32c CPU to FLASH for boards with 45F chip.
Upload is slow, takes about 15 minutes

    usb-jtag/linux/FleaFPGA-JTAG fpga/f32c/f32c-45k-vector/f32c-ulx3s-45k-vector-flash.vme

for boards with 85F chip:

    usb-jtag/linux/FleaFPGA-JTAG fpga/f32c/f32c-85k-vector/f32c-ulx3s-85k-vector-flash.vme

Re-plug USB. If HDMI monitor is connected, a color test screen 640x480 should appear.
Upload self-test binary executable

    fpga/f32c/f32cup.py fpga/f32c/f32c-bin/selftest1.bin

ULX3S should blink LEDs and print test results on usbserial 115200,8,N,1 and monitor.

    stty sane 115200 < /dev/ttyUSB0
    cat /dev/ttyUSB0

RTC clock should advance. CRC OK should be displayed if monitor is connected.
ADC readings 1000 and 1FFF should alternate.
Holding pushbuttons and changing DIP switches should change value at BTN and SW.
It should look like this

    2018-01-01 00:12:16 ALM *-01 00:00:00
    EDID EEPROM:128 CRC=00 OK
    0000 1000 2000 3000 4000 5000 6000 7000
    BTN:_______ SW:1234 LED:_6543210
    2018-01-01 00:12:19 ALM *-01 00:00:00
    EDID EEPROM:128 CRC=00 OK
    0000 1ff0 2000 3ff0 4000 5ff0 6000 7ff0
    BTN:_______ SW:1234 LED:76543210

Upload pass-thru bitstream to FPGA config flash

    usb-jtag/linux/FleaFPGA-JTAG fpga/passthru-v18/passthru-45k-flash.vme

Re-plug USB, some LEDs will be lit by passthru bitstream.
Burn ESP32 efuse to ignore GPIO12 and fix flash voltage to 3.3V

    cd esp32
    ./burn-efuse-flash-3v3.sh

Upload ESP32 websvf application and SPI filesystem to ESP32

    cd esp32
    ./upload-executable.sh
    ./upload-spiffs.sh

Start websvf in open AP mode:
Unplug USB, while keeping BTN0 pressed, plug USB. After blue LED
blinks once (lit for 0.5 seconds), release BTN0.

Web opration without SD: Connect to the AP (SSID:websvf). Open web browser
"firefox", open page http://192.168.4.1 and from there SVF files can be uploaded
directly to FPGA.

Web operation with SD: Place a SD card, FAT32 formatted with first partiton max 4GB. and
Content of SD card can be managed using web interface. Directories can be browsed, 
files uploaded and deleted, SVF files programmed to FPGA.

Standalone operation: connect OLED SSD1331 and press and hold BTN0 
for 2 seconds, a directory content will be shown on OLED. Files can
be browsed and SVF uploaded using OLED and onboard buttons.
