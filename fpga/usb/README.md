# USB HID demo

Plug into US2 or on side adapter US3, US4 some 
USB1.0 (low-speed) device like
mouse, keyboard, joystick.

USB reports will be displayed as HEX numbers
on both DVI monitor and ST7789 LCD.

Pressing keys should change HEX numbers.

Programming examples

    zcat ulx3s_12f_usbhost_test.bit.gz | fujprog

or

    gunzip ulx3s_12f_usbhost_test.bit.gz
    fujprog ulx3s_12f_usbhost_test.bit

or

    gunzip ulx3s_12f_usbhost_test.bit.gz
    openFPGALoader --board ulx3s ulx3s_12f_usbhost_test.bit
