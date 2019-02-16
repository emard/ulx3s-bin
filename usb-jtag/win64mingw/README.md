# win64 binaries

You need to install [FTDI D2XX CDM Driver](https://www.ftdichip.com/Drivers/D2XX.htm)
and try if ujprog works.

"ujprog.exe" is compiled on linux for win64 target using mingw cross
compiler.

Sometimes installing the FTDI driver is not enough, and ujprog needs
"amd64/ftd2xx64.dll" library unzipped and copied to the same directory where
"ujprog.exe" is.

    unzip CDM*Certified.zip amd64/ftd2xx64.dll
