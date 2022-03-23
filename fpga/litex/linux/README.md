### Linux on Litex for ULX3S bitstream and linux

Read more about linux on litex here: https://github.com/litex-hub/linux-on-litex-vexriscv

Extract zip files to root of FAT32 SD card

Place the card into ULX3S

Upload bitstream to ULX3S

```
fujprog ulx3s_50MHz_linux.bit
```

or permanently in flash with 

```
fujprog -j flash ulx3s_50MHz_linux.bit
```

If ULX3S serial is on ttyUSB0 you can connect to serial with

```
screen /dev/ttyUSB0 115200 
```

BTI1 on ULX3S is set as reset so if you do not see anything starting press BT1 shortly

You may need to add sudo if user is not member of dialout group

Framebuffer on GPDI should show penguin

You can fill framebuffer with raw data

You can mount SDCARD with

```
mount /dev/mmcblk0p1 /mnt
```

Then you copy file to the system from SDCARD

```
cp /mnt/framebuff.raw ulx4m.raw
```

After that you just need to send raw file to fb1

```
cat ulx4m.raw /dev/fb0
```

If you want to convert you own picture you can do it on your computer with this

```
convert yourPic.jpg -size 640x480 -depth 8 RGBA:framebuff.raw
```
