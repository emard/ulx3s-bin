# Oscilloscope demo for ULX3S

Here are demo binaries compiled from hdl4fpga sources for ULX3S.
Turns ULX3S into a 4-channel storage oscilloscope with GUI.
It will show traces on 96x64 color OLED or 800x600 on digital monitor.


# GUI

User can control the oscilloscope it with PS/2 mouse connected
to US2 port. There are thigs to click:


    GRID
    main window where traces are
    ----------------------------
    wheel       : move trigger level up/down by 1 pixel
    left drag   : move trigger level up/down by 1 pixel
    left click  : set trigger level
    right click : freeze display after next trigger event
    wheel click : change trigger edge rising/falling


    VERTICAL SETTINGS
    vertical scale window with numbers, left of the grid
    ---------------------
    wheel       : gain, forward=zoom in (mV), backward=zoom out (V)
    left drag   : move trace up/down by 1 pixel
    right drag  : move trace up/down by 1 div
    left click  : set trigger level


    HORIZONTAL SETTINGS
    horizontal scale window with numbers, below the grid
    --------------
    wheel       : timebase, forward=zoom in (us), backward=zoom out (s)
    left drag   : move trace left/right by 1 pixel
    right click : freeze display after next trigger event
    wheel click : change trigger edge rising/falling


    SELECT CHANNEL
    color box below vertical scale and left of horizontal scale
    -----------------------------------------------------------
    wheel       : channel up/down

If mouse doesn't work at power-up, try to first start the
bitstream and then plug the mouse. Combo mouse PS/2 and USB 
need to receive PS/2 protocol quicky after power up otherwise
it will switch to USB mode. Only 12F in single boot mode
can start bitstream fast enough for the mouse to enter PS/2 mode.
For all multiboot and 85F, combo protocol mouse must be plugged
after the bitstream has started.

By default oscilloscope is set to maximum sensitivity (mV)
and fastest (shortest) time base (us).

# Input

Electrical inputs are 0-3.3V relative to GND differential.
Never apply negative input below GND=0V or positive above VCC=3.3V

    GP is differential NEGATIVE
    GN is differential POSITIVE
    ----- --  ------
    GP,GN 14  YELLOW
    GP,GN 15  BLUE
    GP,GN 16  GREEN
    GP,GN 17  VIOLET

Onboard 8-12 bit ADC samples data at rate of 156250 Hz (sa/s).

The numeric scale currently doesn't relate by any calibrated
factor to actual voltage and time physical values.

# Signal generator

Onboard variable frequency signal generator.
By holding BTN3-5 FPGA can apply test signal
of kinda digital-sine approximaion going "0,+1,0,-1"
to each differential pair over shared pins that
are common to ADC and FPGA. You don't need to 
connect anything, Just hold BTN3-4.

    BTN1    FREQ UP
    BTN2    FREQ DOWN
    BTN3    YELLOW
    BTN4    BLUE
    BTN5    GREEN
    BTN6    VIOLET

# Multiboot

Here is also prepared compiled multiboot image containing both
OLED and DVI image. Flash it with

    ujprog -j flash ulx3s_85f_scope_oled_dvi.bit

User can alternate between OLED and DVI by pressing BTN0:

    BTN0    OLED/DVI change

After switching multiboot image, all oscilloscpe settings will
be reset to their default values.
