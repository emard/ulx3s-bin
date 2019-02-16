# win32 binaries

You need to install [FTDI CDM Driver](https://www.ftdichip.com/Drivers/CDM)
and try if ujprog works.

Sometimes installing FTDI driver is not enough, and ujprog needs
"i386/ftd2xx.dll" library unzipped and copied to same directory where
"ujprog.exe" is.

    unzip CDM*Certified.zip i386/ftd2xx.dll
