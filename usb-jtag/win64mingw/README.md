# win64 binaries

You need to install [FTDI CDM Driver](https://www.ftdichip.com/Drivers/CDM)
and try if ujprog works.

Sometimes installing the FTDI driver is not enough, and ujprog needs
"amd64/ftd2xx64.dll" library unzipped and copied to the same directory where
"ujprog.exe" is.

    unzip CDM*Certified.zip amd64/ftd2xx64.dll
