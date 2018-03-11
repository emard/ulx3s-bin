# ULX3S binaries

A collection of functional binary files and uploaders
to quickstart with ULX3S. Tested on Debian Linux.

Set ftdi usbserial name

    usb-jtag/linux/ftx_prog --max-bus-power 500
    usb-jtag/linux/ftx_prog --manufacturer "FER-RADIONA-EMARD"
    usb-jtag/linux/ftx_prog --product "ULX3S FPGA 45K v1.7"

Re-plug USB, device will appear with above name.
Upload pass-thru bitstream to FPGA config flash

    usb-jtag/linux/FleaFPGA-JTAG fpga/passthru-v18/passthru-45k-flash.vme

Re-plug USB, some LEDs will be lit by passthru bitstream.
Upload ESP32 websvf application and SPI filesystem to ESP32

    cd esp32
    ./upload-executable.sh
    ./upload-spiffs.sh

Start websvf in open AP mode:
Unplug USB, while keeping BTN0 pressed, plug USB. After blue LED
blinks once (lit for 0.5 seconds), release BTN0.

Web opration without SD: Connect to the AP (SSID:websvf), with firefox browser 
open page 192.168.4.1 and from there SVF files can be uploaded directly to FPGA.

Web operation with SD: Place a SD card, FAT32 formatted with first partiton max 4GB. and
Content of SD card can be managed using web interface from page 192.168.4.1. 
Directories can be browsed, files uploaded and deleted, SVF files programmed to FPGA.

Standalone operation: connect OLED SSD1331 and press and hold BTN0 
for 2 seconds, a directory content will be shown on OLED. Files can
be browsed and SVF uploaded using OLED and onboard buttons.
