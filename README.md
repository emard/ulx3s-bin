# ULX3S binaries

A collection of functional binary files and uploaders
to quickstart with ULX3S. Tested on Debian Linux.

Set ftdi usbserial name

    usb-jtag/linux/ftx_prog --max-bus-power 500
    usb-jtag/linux/ftx_prog --manufacturer "FER-RADIONA-EMARD"
    usb-jtag/linux/ftx_prog --product "ULX3S FPGA 45K v1.7"

Re-plug USB, device will appear with above name.
Upload pass-thru bitstream to FPGA config flash

    FleaFPGA-JTAG fpga/passthru-v18/passthru-45k-flash.vme

Re-plug USB, some LEDs will be lit by passthru bitstream.
Upload ESP32 websvf application and SPI filesystem to ESP32

    cd esp32
    ./upload-executable.sh
    ./upload-spiffs.sh

Start websvf in open AP mode:
Unplug USB, while keeping BTN0 pressed, plug USB. After blue LED
blinks once shortly release BTN0.

Connect to the AP (SSID:websvf), with firefox browser open page
192.168.4.1 and from there SVF files can be uploaded directly to FPGA.

Place a SD card, FAT32 formatted with first partiton max 4GB, and
with web interface content of SD card be managed, directory listed,
files uploaded and deleted, and SVF programmed to FPGA on a mouse click.

Connect OLED SSD1331 and press and hold BTN0 for 2 seconds,
then then files can be browsed and upload with OLED and onboard buttons.
