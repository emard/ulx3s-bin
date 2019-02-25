# SDRAM latency 2-2-2 or 3-3-3

On some boards, selftest may have issues and will work 
only with specific SDRAM latency setting, either 2-2-2 or 3-3-3.

And it's not that some boards have faster or slower SDRAM.
All 85F boards have chips of speed grade 6E, they can do 3-3-3
at 167 MHz, and should have no problem with 2-2-2 at 100 MHz.
It is because of f32c selftest soft-core, for which 100 MHz
in some cases means too much overclock.

bitstream with RAS-CAS-PRE = 2-2-2
ulx3s_v20_85f_f32c_selftest_100mhz.bit

bitstream with RAS-CAS-PRE = 3-3-3
ulx3s_v20_85f_f32c_selftest_100mhz_333.bit
