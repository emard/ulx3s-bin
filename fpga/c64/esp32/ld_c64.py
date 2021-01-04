# micropython ESP32
# C64 PRG loader

# AUTHOR=EMARD
# LICENSE=BSD

from struct import pack,unpack
from time import sleep_ms

class ld_c64:
  def __init__(self,spi,cs):
    self.spi=spi
    self.cs=cs
    self.cs.off()

  def ctrl(self,i):
    self.cs.on()
    self.spi.write(bytearray([0, 0xFF, 0xFF, 0xFF, 0xFF, i]))
    self.cs.off()

  def cpu_halt(self):
    self.ctrl(2)

  def cpu_reset_halt(self):
    self.ctrl(3)

  def cpu_continue(self):
    self.ctrl(0)

  def poke(self,addr,data):
    self.cs.on()
    self.spi.write(bytearray([0,(addr>>24)&0xFF,(addr>>16)&0xFF,(addr>>8)&0xFF,addr&0xFF]))
    self.spi.write(data)
    self.cs.off()

  def peek(self,addr,buffer):
    self.cs.on()
    self.spi.write(bytearray([1,(addr>>24)&0xFF,(addr>>16)&0xFF,(addr>>8)&0xFF,addr&0xFF,0]))
    self.spi.readinto(buffer)
    self.cs.off()

  def type(self,keybuf):
    # fill keyboard buffer as if RUN <ENTER> has been typed
    self.cpu_halt()
    self.poke(0x277,keybuf)
    self.poke(0xC6,bytearray([len(keybuf)]))
    self.cpu_continue()

  # read from file -> write to SPI RAM
  def load_stream(self, filedata, addr=0, maxlen=0x10000, blocksize=1024):
    block = bytearray(blocksize)
    # Request load
    self.cs.on()
    self.spi.write(bytearray([0,(addr >> 24) & 0xFF, (addr >> 16) & 0xFF, (addr >> 8) & 0xFF, addr & 0xFF]))
    bytes_loaded = 0
    while bytes_loaded < maxlen:
      if filedata.readinto(block):
        self.spi.write(block)
        bytes_loaded += blocksize
      else:
        break
    self.cs.off()
    return bytes_loaded

  # "intelligent" PRG loader
  def loadprg_stream(self,f):
    header=bytearray(2)
    f.readinto(header)
    addr=unpack("<H",header)[0]
    self.cpu_halt()
    ROM = (addr==0x8000 or addr==0xA000 or addr==0xE000)
    CART = False
    # for cold boot, delete magic value from 0x8004
    self.poke(0x8004,bytearray(5))
    if not ROM:
      self.cpu_reset_halt()
      self.cpu_halt()
      self.cpu_continue()
      # wait for READY
      sleep_ms(3000)
      self.cpu_halt()
    # LOAD PRG to RAM
    bytes=self.load_stream(f,addr,maxlen=0x10000,blocksize=1)
    # if RAM area loaded, patch RAM as if LOAD command executed
    if not CART:
      #print("set pointers after LOAD %04X-%04X" % (addr,addr+bytes))
      self.poke(0x7A,pack("<H",addr-1))
      self.poke(0x2B,pack("<H",addr))
      self.poke(0x2D,pack("<H",addr+bytes))
      # perform CLR
      self.poke(0x2F,pack("<H",addr+bytes))
      self.poke(0x31,pack("<H",addr+bytes))
      endmem=bytearray(2)
      self.peek(0x37,endmem)
      self.poke(0x33,endmem)
      self.poke(0x3E,bytearray([0])) # clear continue pointer high byte
      self.poke(0x10,bytearray([0])) # clear subscript/FNX flag
      self.type("RUN\r")
    # if ROM cartridge content loaded, start it with reset
    if ROM:
      self.cpu_reset_halt()
      self.cpu_halt()
    self.cpu_continue()
    return bytes

  def loadprg(self,filename):
    return self.loadprg_stream(open(filename,"rb"))
