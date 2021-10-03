# DFU bootloader for ULX3S

This bootloader makes passthru at US1 port for ESP32 flashing
and USB DFU at US2 port for FPGA flashing. DFU is very fast.
Source is based on [HAD2019 badge bootloader](https://github.com/smunaut/had2019-playground)
modified to [ULX3S bootloader](https://github.com/emard/had2019-playground)

To install new bootloader for the first time (5 minutes flashing)
choose bitstream for your board and:

    fujprog -j flash multiboot.img

or

    openFPGALoader -b ulx3s --file-type bin -f multiboot.img

To enter bootloader, hold BTN1 and plug US2
In bootloader mode, LEDs 0-2 should be ON, other LEDs 3-7 OFF:

|   D7   |   D6   |   D5   |   D4   |   D3   |    D2   |    D1   |    D0   |
|--------|--------|--------|--------|--------|---------|---------|---------|
|&#x2b1b;|&#x2b1b;|&#x2b1b;|&#x2b1b;|&#x2b1b;|&#x1f7e9;|&#x1f7e7;|&#x1f7e5;|

Depending on USB and RTC state (low power sleep),
board may not immediately power on when US2 is plugged.
If board doesn't power on from US2:

    Option 1: additionaly plug US1
    Option 2: hold BTN1 as "shift" key and shortly press BTN0 for board to power ON

DFU should enumerate on US2 port:

    less /var/log/syslog
    [138611.358798] usb 1-9.1: new full-speed USB device number 109 using xhci_hcd
    [138611.462365] usb 1-9.1: New USB device found, idVendor=1d50, idProduct=614b, bcdDevice= 0.05
    [138611.462380] usb 1-9.1: New USB device strings: Mfr=2, Product=3, SerialNumber=1
    [138611.462387] usb 1-9.1: Product: ULX3S FPGA (DFU)
    [138611.462392] usb 1-9.1: Manufacturer: FER-RADIONA-EMARD
    [138611.462396] usb 1-9.1: SerialNumber: 5031473636340015

    lsusb
    Bus 001 Device 117: ID 1d50:614b OpenMoko, Inc. ULX3S FPGA (DFU)

On linux, it's practical to add a udev rule which allows normal users
members of "dialout" group to also run dfu-util,
otherwise it should be run as root:

    # file: /etc/udev/rules.d/80-fpga-dfu.rules
    # this is for DFU 1d50:614b libusb access
    ATTRS{idVendor}=="1d50", ATTRS{idProduct}=="614b", \
    GROUP="dialout", MODE="666"

To upload and start user bitstream (fast, few seconds):

    dfu-util -a 0 -R -D blink.bit

To upgrade bootloader (fast, few seconds)

    dfu-util -a 5 -D bootloader.bit

To list all flashing destinations for -a N

    dfu-util -l
