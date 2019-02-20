# win32 binaries

You need to install [FTDI D2XX CDM Driver](https://www.ftdichip.com/Drivers/D2XX.htm)
and try if ujprog works.

"ujprog.exe" is compiled on linux for win32 target using mingw cross
compiler.

Sometimes installing FTDI driver is not enough, and ujprog needs
"i386/ftd2xx.dll" library unzipped and copied to the same directory where
"ujprog.exe" is.

    unzip CDM*Certified.zip i386/ftd2xx.dll
