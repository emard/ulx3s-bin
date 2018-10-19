# ULX3S binaries

A collection of functional binary files and uploaders
to quickstart with ULX3S. Works from Debian Linux.
Connect USB PC port with micro-USB cable to US1 port of ULX3S.
FT231X in factory default state should turn ON Green LED D18
when connected to PC.

Set ftdi usbserial name

    usb-jtag/linux/ftx_prog --max-bus-power 500
    usb-jtag/linux/ftx_prog --manufacturer "FER-RADIONA-EMARD"
    usb-jtag/linux/ftx_prog --product "ULX3S FPGA 12K v3.0.3"
    usb-jtag/linux/ftx_prog --new-serial-number 120001
    usb-jtag/linux/ftx_prog --cbus 2 TxRxLED
    usb-jtag/linux/ftx_prog --cbus 3 SLEEP

Re-plug USB, device should appear with above name. 
USB-JTAG programmer "ujprog" accepts "*.bit" or "*.svf" files,
programmer "FleaFPGA-JTAG" accepts "*.vme" files.
Programmer will recognize product string and treat 
"12K", "25K", "45K" or "85K" the same way.
Upload f32c CPU appropriate for 12F/25F/45F/85F chip, example:

    usb-jtag/linux/ujprog fpga/f32c/f32c-12k-v20/f32c_ulx3s_v20_12k_selftest_100mhz.bit
    usb-jtag/win32/ujprog.exe fpga/f32c/f32c-25k-vector-v20/f32c_selftest_ulx3s_v20_25k.bit
    usb-jtag/linux/FleaFPGA-JTAG fpga/f32c/f32c-45k-vector-v20/f32c_selftest_ulx3s_v20_45k_sram.vme
    usb-jtag/win32/FleaFPGA-JTAG.exe fpga/f32c/f32c-85k-vector-v20/f32c_selftest_ulx3s_v20_85k_sram.vme

Re-plug USB. If HDMI monitor is connected, a color test screen 640x480 should
appear. Upload self-test binary executable

    fpga/f32c/f32cup.py fpga/f32c/f32c-bin/selftest-mcp7940n.bin

Upload progess will be printed

    f32c python uploader (under construction)
    MIPS Little-Endian header received
    ADDR 0x80000000 LEN 8208 CRC 0xF17DE856 OK
    ADDR 0x80002010 LEN 8192 CRC 0x58788D1D OK
    ADDR 0x80004010 LEN 6124 CRC 0xC922F84A OK
    JUMP 0x80000000

ULX3S should blink LEDs and print test results on usbserial 115200,8,N,1

    stty sane 115200 < /dev/ttyUSB0
    cat /dev/ttyUSB0

RTC clock should advance. CRC OK should be displayed if monitor is connected.
ADC readings should alternate from 1000 to 1FF0.
Holding pushbuttons and changing DIP switches should change value at BTN and SW.
It should look like this

    2018-01-01 00:10:31  OK  *-01 00:00:00
    EDID EEPROM:128 CRC=00 OK
    0ff0 1000 2ff0 3000 4ff0 5000 6ff0 7000
     OK   OK   OK   OK   OK   OK   OK   OK 
    DAC: L3210  OK  R3210  OK  V3210  OK 
    BTN:_12____ SW:1234 LED:___4___0
    2018-01-01 00:10:33  OK  *-01 00:00:00
    EDID EEPROM:128 CRC=00 OK
    0000 1ff0 2000 3ff0 4000 5ff0 6000 7ff0
     OK   OK   OK   OK   OK   OK   OK   OK 
    DAC: L3210  OK  R3210  OK  V3210  OK 
    BTN:___34__ SW:1234 LED:__5___1_

Same content as printed on usbserial should also be shown on HDMI monitor
on screen with black background and white letters. 
If above self test looks good, board is useable.
upload pass-thru bitstream to FPGA config flash

    usb-jtag/linux/FleaFPGA-JTAG fpga/passthru-v18/passthru-45k-flash.vme

Re-plug USB, some LEDs will be lit by passthru bitstream.
Make sure SD card is not yet inserted.
To allow programming ESP32 when SD card is inserted,
burn efuse to ignore GPIO12 and fix flash voltage to 3.3V

    cd esp32
    ./burn-efuse-flash-3v3.sh

Upload ESP32 websvf application and SPI filesystem to ESP32
(choose appropriate for 12F/25F/45F/85F chip)

    cd esp32
    ./upload-executable.sh
    ./upload-spiffs.sh websvf_sd/websvf_sd_v20_12f.spiffs.bin

If upload fails with error or doesn't progress, press Ctrl-C and
retry until it succeeds with:

    Hash of data verified.

To Start websvf in open AP mode: Unplug USB, while keeping BTN0 pressed,
plug USB. After blue LED blinks once (lit for 0.5 seconds), quickly release BTN0.
This procedure sometimes needs to be applied also to reflash ESP32 and to prevent
ESP32 autoexec at power-on when following two files exist:

    /ULX3S/f32c/autoexec/f32c.svf      # f32c bitstream for autoexec
    /ULX3S/f32c/autoexec/autoexec.bit  # f32c binary executable

Web opration without SD: Connect to the AP (SSID:websvf). Open web browser
"firefox", open page http://192.168.4.1 and from there SVF files can be uploaded
directly to FPGA.

Web operation with SD: Place a SD card, FAT32 formatted with first partiton max 4GB. and
Content of SD card can be managed using web interface. Directories can be browsed, 
files uploaded and deleted, SVF files programmed to FPGA.

Standalone operation: connect OLED SSD1331 and press and hold BTN0 
for 2 seconds, a directory content will be shown on OLED. Files can
be browsed and SVF uploaded using OLED and onboard buttons.

Wake up on RTC: Turn off green LED D18

    usb-jtag/linux/ftx_prog --cbus 3 DRIVE_0

After USB is re-plugged, D18 should be OFF. If D18 is ON the board is always
ON. If D18 is OFF, the board can enter shutdown state and wake up on RTC.
Put 3V battery CR1225 in (respect polarity) and set RTC current time,
alarm time, enable alarm and set alarm output pin polarity as active LOW.
If alarm is not yet triggered, LED D11 (found on back side of the board near J1
pin 22) should be very dimly lit, visible in dark.
When alarm is triggered, D11 should be off. While D11 is dimly lit, power down 
board by setting SHUTDOWN signal to 1 or shortly connect R13 to 3.3V.
When alarm is triggered, board should turn on.

# OpenOCD

Besides FleaFPGA-JTAG, ULX3S can be programmed using OpenOCD too.
External JTAG like FT2232 can be used, but in recent OpenOCD
there is FT232R driver which can be patched to work with onboard
FT231X. It works but FleaFPGA-JTAG is much faster.

[Source openOCD FT232R](https://github.com/emard/openocd).
can be compiled into
[Binary OpenOCD FT232R](/usb-jtag/linux/openocd)
using this shell commands:

    cd openocd
    ./bootstrap
    mkdir build
    cd build
    ../configure
    make

OpenOCD config files for ULX3S boards:

ft231x.ocd

    interface ft232r
    ft232r_vid_pid 0x0403 0x6015
    # ULX3S specific GPIO setting
    ft232r_tck_num DSR
    ft232r_tms_num DCD
    ft232r_tdi_num RI
    ft232r_tdo_num CTS
    # trst/srst are not used but must have different values than above
    ft232r_trst_num RTS
    ft232r_srst_num DTR
    adapter_khz 1000

ecp5-XXf.cfg

    telnet_port 4444
    gdb_port 3333

    # JTAG TAPs
    jtag newtap lfe5u12 tap -expected-id 0x21111043 -irlen 8 -irmask 0xFF -ircapture 0x5
    #jtag newtap lfe5u25 tap -expected-id 0x41111043 -irlen 8 -irmask 0xFF -ircapture 0x5
    #jtag newtap lfe5u45 tap -expected-id 0x41112043 -irlen 8 -irmask 0xFF -ircapture 0x5
    #jtag newtap lfe5u85 tap -expected-id 0x41113043 -irlen 8 -irmask 0xFF -ircapture 0x5

    init
    scan_chain
    svf -tap lfe5u12.tap -quiet -progress bitstream.svf
    shutdown

OpenOCD at start should detect JTAG ID of the FPGA chip, something like this

    ./openocd --file=ft231x.ocd --file=ecp5-XXf.cfg

    FT232R num: TCK = 5 DSR
    FT232R num: TMS = 6 DCD
    FT232R num: TDI = 7 RI
    FT232R num: TDO = 3 CTS
    FT232R num: TRST = 2 RTS
    FT232R num: SRST = 4 DTR
    adapter speed: 1000 kHz
    Info : JTAG tap: lfe5u12.tap tap/device found: 0x21111043 (mfg: 0x021 (Lattice Semi.), part: 0x1111, ver: 0x2)
       TapName             Enabled  IdCode     Expected   IrLen IrCap IrMask
    -- ------------------- -------- ---------- ---------- ----- ----- ------
     0 lfe5u12.tap            Y     0x21111043 0x21111043     8 0x05  0xff
    svf processing file: "bitstream.svf"

# Troubleshooting

If manually soldering, solder first BGA chip and check all of
its connections using universal instrument set to diode test.

Connect it reverse: (+) RED wire to GND of PCB, probe FPGA
pins connectivity with (-) BLACK wire. A reading of 0.5-0.7 V
indicate proper electrical connection to BGA. It comes from
the voltage drop of reverse polarity protection diodes
in the silicon wafer architecture. Such diodes exist
on every pin.

Most important is that all JTAG pins have connection.
If JTAG didn't make connection but if FLASH pins are good
then it is possible to externally program FLASH bootloader
and have some use of the board over US2 port.

FPGA chip soldered on PCB without any other parts
should respond to JTAG commands if proper supply voltages
1.1V, 2.5V, 3.3V are connected. It will respond with JTAG ID
and will also accept programming with suitable bitstream.
No clock, no capacitors, no resistors nothing else is required
for this test, just BGA soldered.

If this test passes, proceed with soldering rest of components.
Solder "power" and "usb" section and try programming
using US1 port. Don't forget diode D8 at "usb" section, it
forwards 5V USB supply to the power section.

Before plugging to US1 power, First cut the RP1,2,3 jumpers open
to prevent wrong voltages being initally applied to rest of the board.
Measure voltages at jumpers:

    RP1: 1.1V
    RP2: 2.5V
    RP3: 3.3V

If this voltages are OK (should be within 2% accuracy)
then close jumpers, the voltage will be found at capacitors under BGA:

    C17: 1.1V
    C19: 2.5V
    C20: 3.3V

Powered but unprogrammed FPGA chip should not generate any heat noticeable by
touch of a finger and whole board in initial state should draw less than 50mA.
On top side, green LED D18 should be ON, other LEDs OFF. 
