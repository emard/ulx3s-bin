# DFU bootloader for ULX3S

This bootloader makes passthru at US1 port for ESP32 flashing
and USB DFU at US2 port for FPGA flashing. DFU is very fast.

To install new bootloader (5-10 min)

    fujprog -j flash multiboot.img

to enter bootloader, hold BTN1 and plug US2
(if board doesn't power up press BTN0).
In bootloader mode, LEDs 0-2 should be ON, LEDs 3-7 OFF.

To upload and start user bitstream:

    dfu-util -a 0 -R -D blink.bit

To upgrade bootloader

    dfu-util -a 5 -D bootloader.bit

To list all flashing destinations for -a N

    dfu-util -l
