#!/usr/bin/env python3

import os
import sys
import getopt
import serial
import time
import struct


print("f32c python uploader v1.0")
f32c_serial_device_name = "/dev/ttyUSB0"
f32c_filename = sys.argv[-1]

# byte length of chunked file read and upload
chunksize = 8192
# seconds to hold serial break
serial_break_duration = 0.12
# bps serial
serial_baud_default = 115200 # normal f32c prompt speed after reset (don't touch)
serial_baud_upload = 115200 # upload speed - 115200 or 3000000 (3 Mbit)
# seconds for serial port timeout
serial_timeout = 0.2
# serial file open descriptor
serial_port = None
# file open descriptor
input_fd = None

def get_cmdline_options():
 global opts
 global extraparams
 
 global chunksize
 global serial_break_duration
 global serial_baud_default
 global serial_baud_upload
 global f32c_filename
 global f32c_serial_device_name

 opts, extraparams = getopt.getopt(
     sys.argv[1:],
     'p:b:f:',
     ['port=', 'baud=', 'break=', 'chunk=', 'file=']
 )
   
 for o,p in opts:
  if o in ['-b','--baud']:
   serial_baud_upload = int(float(p)+0.5)
  if o in ['--chunk']:
   chunksize = int(p)
  elif o in ['--break']:
   serial_break_duration = float(p)
  elif o in ['-f','--file']:
   f32c_filename = p
  elif o in ['-p','--port']:
   f32c_serial_device_name = p


def parse_cmd_options():
  return

# keep on resetting several times
# by sending serial break until
# prompt is received or give up
def try_to_get_prompt(retries = 2):
  global serial_port
  while retries > 0:
    serial_port.reset_input_buffer()
    serial_port.reset_output_buffer()
    serial_port.send_break(duration = serial_break_duration)
    reply = serial_port.read(20)
    if reply.find(b"m32l> "):
      return 1 # MIPS little-endian prompt is found
    #if reply.find(b"m32b> "):
    #  return 2 # MIPS big-endian prompt is found (unsupported)
    if reply.find(b"rv32> "):
      return 5 # RISC-V prompt is found
    print(reply)
    print("retry %d" % (retries,) )
    retries -= 1
  return 0 # prompt not found


# calculate block's CRC  
def crc_block(chunk):
  crc = 0
  for byte in chunk:
   crc = ((crc >> 31) | (crc << 1))
   crc = (crc + byte) & 0xFFFFFFFF
  return crc

  
def receive_crc(retry_crc = 4, sleep_s = 10.0e-3):
  global serial_port
  crc = (None, )
  while retry_crc > 0:
      if (retry_crc & 0) == 0: # every other retry time request checksum
        serial_port.reset_input_buffer()
        serial_port.reset_output_buffer()
        serial_port.write(b"\x81") # request to read checksum
      read_crc = serial_port.read(4) # read 4 bytes of potential CRC response
      if len(read_crc) == 4:
        # print(read_crc)
        crc = struct.unpack(">L", read_crc)
        break
      #else:
      #  print(read_crc)
      time.sleep(sleep_s) # after not receiving, sleep 10 ms
      retry_crc -= 1 # decrement and try again to receive crc
  return crc[0]


def upload_block(addr, chunk, first = True, retry_block = 5, retry_crc = 4):
  global serial_port
  global serial_baud_default
  global serial_baud_upload
  # print("%08X" % addr)
  length = len(chunk)
  expected_crc = crc_block(chunk)
  # print("BASE=%08X CRC=%08X LEN=%d" % (addr, expected_crc, length) )
  while retry_block > 0:
    # first block will reset f32c and initialize binary transfer
    if first:
      serial_port.baudrate = serial_baud_default
      if try_to_get_prompt() > 0:
        serial_port.write(b"\xFF") # request binary upload
        # change baudrate if not default
        if serial_baud_upload != serial_baud_default:
          header = b"\x80" + struct.pack(">L", serial_baud_upload) + b"\xb0"
          serial_port.write(header)
          time.sleep(50.0e-3)
          serial_port.baudrate = serial_baud_upload
      else:
        break # go to retry
    # construct header that requests block upload packet,
    # with encoded length and block start address
    serial_port.reset_input_buffer()
    serial_port.reset_output_buffer()
    header = b"\x80" + struct.pack(">L", length) + b"\x90" \
           + b"\x80" + struct.pack(">L", addr) + b"\xA0"
    serial_port.write(header + chunk)
    received_crc = receive_crc()
    if received_crc != None:
      if received_crc == expected_crc:
        print("ADDR 0x%08X LEN %d CRC 0x%08X OK" % (addr, length, expected_crc) )
        return 1 # success
      else:
        # print("crc mismatch")
        print("ADDR 0x%08X LEN %d CRC expected:0x%08X, received:0x%08X RETRY %d" % (addr, length, expected_crc, received_crc, retry_block,) )
    else:
      # serial_port.write(b"\xFF") # request binary upload
      # time.sleep(0.1)
      print("CRC not received, RETRY %d" % retry_block)
    retry_block -= 1
  return 0 # failure after retries


def jump(start_address):
  global serial_port
  header = b"\x80" + struct.pack(">L", start_address) + b"\xb1"
  serial_port.write(header)


def read_upload_jump():
  global f32c_filename
  input_fd=open(os.path.expanduser(f32c_filename), "rb")
  if input_fd:
   # HEADER: read first 16 bytes from input file
   # to determine file type and start address
   header = input_fd.read(16)
   start_address = 0
   if  header[2:4]   == b"\x10\x3C" \
   and header[6:8]   == b"\x10\x26" \
   and header[10:12] == b"\x11\x3C" \
   and header[14:16] == b"\x31\x26":
     print("MIPS Little-Endian header received")
     start_address = (header[1] << 24) + (header[0] << 16) + (header[5] << 8) + header[4]
   if  header[0:2]   == b"\x97\x0F" \
   and header[4:6]   == b"\x93\x81":
     print("RISC-V Little-Endian header received")
     start_address = 0x400 # FIXME HARDCODED LOAD ADDRESS FIXME
   # print("start_address:0x%08X" % start_address)
   chunk = header
   block_start = start_address
   success = 1 # assume success
   while True:
    chunk += input_fd.read(chunksize)
    if not chunk:
        break
    if upload_block(block_start, chunk, first=(block_start==start_address) ) == 0:
        success = 0 # failure, don't jumo
        break
    block_start += len(chunk)
    chunk = b""
  input_fd.close()
  # return serial port to default baudrate before starting the binary
  if serial_baud_upload != serial_baud_default:
          header = b"\x80" + struct.pack(">L", serial_baud_default) + b"\xb0"
          serial_port.write(header)
          time.sleep(50.0e-3)
          serial_port.baudrate = serial_baud_default
  if success > 0:
    jump(start_address)
    print("JUMP 0x%08X" % (start_address,) )


def main():
  global f32c_serial_device_name
  global serial_baud_default
  global serial_port

  get_cmdline_options()
  serial_port=serial.Serial(f32c_serial_device_name, serial_baud_default, rtscts=False, timeout=serial_timeout)
  read_upload_jump()
  serial_port.close()

main()
