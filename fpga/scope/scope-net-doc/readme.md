# SCOPEIO USB Ethernet

Connect PC (linux) to US2. It should enumerate as
full-speed USB CDC ethernet networking device with
MAC 00:aa:bb:cc:dd:ee.
It should appear as a linux network interface named
"enx00aabbccddee".

Give the interface an IP address:

    ifconfig enx00aabbccddee 192.168.18.254

# Bridging USB Ethernet with Wired Ethernet

    brctl addbr br0
    brctl addif br0 enp7s0
    brctl addif br0 enx00aabbccddee
    brctl stp br0 off
    brctl setageing br0 0
    dhclient br0

Press BTN1 tcpdump or wireshark will see packet from DHCP reply.

    ping 192.168.1.207

ping will receive no ICMP response but arp table will be populated:

    arp -an
    ? (192.168.1.207) at 00:40:00:01:02:03 [ether] on br0

Try to export mouse movements as UDP packets... Find the mouse

    lsinput
    /dev/input/event7
       bustype : BUS_USB
       vendor  : 0x46d
       product : 0xc03e
       version : 272
       name    : "Logitech USB-PS/2 Optical Mouse"
       phys    : "usb-0000:00:1d.0-1.3/input0"
       uniq    : ""
       bits ev : (null) (null) (null) (null)

give it user rw permission

    chmod a+rw /dev/input/event7

Edit "hostmouse.py" and put IP adresu (instead of 192.168.1.207)
Run hostmouse:

    ./hostmouse.py
    Found Logitech USB-PS/2 Optical Mouse at /dev/input/event7...
    Sending mouse events to 192.168.1.207:57001
    Started listening to device

# Running local DHCP server

Configure dnsmasq (DHCP) server to listen to 192.168.18.254
and configure it for scopeio networking. From networking point of view,
scopeio will appear as another IP node on the USB network interface. 
PC USB-network interface side should have different MAC and IP address
from the scopeio MAC 00:40:00:01:02:03, even though both are the same 
USB device.

    cat /etc/dnsmasq.d/interface.conf
    listen-address=127.0.0.1
    listen-address=192.168.18.254
    bind-interfaces

    cat /etc/dnsmasq.d/host-scopeio.conf
    dhcp-host=00:40:00:01:02:03,scopeio,192.168.18.186

Start or restart the dnsmasq (DHCP) server:

    service dnsmasq restart

Optionally, you can monitor network traffic with wireshark or tcpdump:

    tcpdump -i enx00aabbccddee -e -XX -n

Press BTN1 on ULX3S (manual request for IP config).
scopeio should request IP address:

    14:02:24.701649 00:40:00:01:02:03 > ff:ff:ff:ff:ff:ff, ethertype IPv4 (0x0800), length 296: 0.0.0.0.68 > 255.255.255.255.67: BOOTP/DHCP, Request from 00:40:00:01:02:03, length 250
	0x0000:  ffff ffff ffff 0040 0001 0203 0800 4500  .......@......E.
	0x0010:  0116 0000 0000 0511 b4d8 0000 0000 ffff  ................
	0x0020:  ffff 0044 0043 0102 d5dc 0101 0600 3903  ...D.C........9.
	0x0030:  f326 0000 0000 0000 0000 0000 0000 0000  .&..............
	0x0040:  0000 0000 0000 0040 0001 0203 0000 0000  .......@........
	0x0050:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x0060:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x0070:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x0080:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x0090:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x00a0:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x00b0:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x00c0:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x00d0:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x00e0:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x00f0:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x0100:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x0110:  0000 0000 0000 6382 5363 3501 0132 0400  ......c.Sc5..2..
	0x0120:  0000 00ff 732c 716b                      ....s,qk

DHCP server should reply, offering IP address 192.168.18.186:

    14:02:27.705669 00:aa:bb:cc:dd:ee > 00:40:00:01:02:03, ethertype IPv4 (0x0800), length 349: 192.168.18.254.67 > 192.168.18.186.68: BOOTP/DHCP, Reply, length 307
	0x0000:  0040 0001 0203 00aa bbcc ddee 0800 45c0  .@............E.
	0x0010:  014f bd1e 0000 4011 14b7 c0a8 12fe c0a8  .O....@.........
	0x0020:  12ba 0043 0044 013b c591 0201 0600 3903  ...C.D.;......9.
	0x0030:  f326 0000 0000 0000 0000 c0a8 12ba c0a8  .&..............
	0x0040:  12fe 0000 0000 0040 0001 0203 0000 0000  .......@........
	0x0050:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x0060:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x0070:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x0080:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x0090:  0000 0000 0000 4241 4e54 2d52 0000 0000  ......BANT-R....
	0x00a0:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x00b0:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x00c0:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x00d0:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x00e0:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x00f0:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x0100:  0000 0000 0000 0000 0000 0000 0000 0000  ................
	0x0110:  0000 0000 0000 6382 5363 3501 0236 04c0  ......c.Sc5..6..
	0x0120:  a812 fe33 0400 000e 103a 0400 0007 083b  ...3.....:.....;
	0x0130:  0400 000c 4e01 04ff ffff 001c 04c0 a812  ....N...........
	0x0140:  ff06 04c0 a812 fe0f 036c 616e 7908 180a  .........lany...
	0x0150:  0000 c0a8 0122 0304 c0a8 12fe ff         .....".......

Then some ARP request from PC should come (if it doesn't then 
ping 192.168.18.186 should make it)

    14:06:26.609070 00:aa:bb:cc:dd:ee > ff:ff:ff:ff:ff:ff, ethertype ARP (0x0806), length 42: Request who-has 192.168.18.186 tell 192.168.18.254, length 28
	0x0000:  ffff ffff ffff 00aa bbcc ddee 0806 0001  ................
	0x0010:  0800 0604 0001 00aa bbcc ddee c0a8 12fe  ................
	0x0020:  0000 0000 0000 c0a8 12ba                 ..........

scopeio should answer ARP with its IP address:

    14:06:34.634887 00:40:00:01:02:03 > ff:ff:ff:ff:ff:ff, ethertype ARP (0x0806), length 64: Reply 192.168.18.186 is-at 00:40:00:01:02:03, length 50
	0x0000:  ffff ffff ffff 0040 0001 0203 0806 0001  .......@........
	0x0010:  0800 0604 0002 0040 0001 0203 c0a8 12ba  .......@........
	0x0020:  ffff ffff ffff c0a8 12ba 0000 0000 0000  ................
	0x0030:  0000 0000 0000 0000 0000 0000 99a5 c267  ...............g

Note that scopeio will not respond to ping's with ICMP echo reply, but from active
ping attempts it will keep linux arp table populated with this:

    arp -an
    ? (192.168.18.186) at 00:40:00:01:02:03 [ether] on enx00aabbccddee

If you got this far, then scopeio UDP networking should work.
Try to export mouse movements as UDP packets... Find the mouse

    lsinput
    /dev/input/event7
       bustype : BUS_USB
       vendor  : 0x46d
       product : 0xc03e
       version : 272
       name    : "Logitech USB-PS/2 Optical Mouse"
       phys    : "usb-0000:00:1d.0-1.3/input0"
       uniq    : ""
       bits ev : (null) (null) (null) (null)

give it user rw permission

    chmod a+rw /dev/input/event7

And run python application that converts linux mouse movements
to UDP packets that control scopeio (C_mouse_host):

    ./hostmouse.py
    Found Logitech USB-PS/2 Optical Mouse at /dev/input/event7...
    Sending mouse events to 192.168.18.186:57001
    Started listening to device
