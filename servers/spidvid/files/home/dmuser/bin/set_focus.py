#!/usr/bin/python
# Rob Fuller, May 2017.
# For commands see:
# file://galwayfs03/Public/cabledObsManuals/Kongsberg-OE14-522-5100-rs232-commands.pdf
#
from serial import rfc2217,serial_for_url,Serial
from time import sleep, gmtime, strftime
import struct
from subprocess import call
import sys


ser = serial_for_url("socket://172.16.255.6:950",9600,timeout=10)
def append_checksum(command):
  checksum = 0
  for el in bytes(command):
    checksum ^= ord(el)
  checksum = bytes(chr(checksum))
  command.append(b":")
  checksum_ind = b"G"
  if checksum == b"\x3c":
    checksum = b"\xff";
    checksum_ind = b"0"
  elif checksum == b"\x3e":
    checksum = b"\xff"
    checksum_ind = b"1"
  command.append(checksum)
  command.append(b":")
  command.append(checksum_ind)
  return command

def create_command(cmd):
  command = bytearray()
  b_to = b"\x02"
  b_from = b"\x01"
  command.append(b_to)
  command.append(b":")
  command.append(b_from)
  command.append(b":")
  length = len(cmd)
  if length > 99:
    length = 99
  command.append(bytes(chr(length)))
  command.append(b":")
  for b in cmd:
    command.append(b)
  return append_checksum(command)

def send(ser,command):
  cmd = create_command(command)
  ser.write(b"<")
  ser.write(cmd)
  ser.write(b">")

def read_message(ser):
  header = ser.read(7)
  command_len = struct.unpack('b',header[5])[0]
  #TODO: if command_len = 99 could be longer...
  command = ser.read(command_len)
  trail = ser.read(5)
  colon_pos = command.index(b':')
  answer = {
      "command": command[0:colon_pos],
      "data": []
   }
  if colon_pos < len(command)-1:
    answer["data"] = command[(colon_pos+1):]
  # TODO: validate header and trailer
  return answer

def read_ack(ser,command):
  message = read_message(ser)
  if message["command"] != '\x06':
    raise Exception("The response from server was not an ack but was {0}".format(message["command"]))
  ack = message["data"][0:len(command)]
  if ack != command:
    raise Exception("The response ack was for {0} but expected {1}".format(ack,command))
  return message["data"][len(command):]

# TODO: move the above copy/pated code to a shared function

# Fast Focus
#send(ser,b":FX:"+b'\x0F')
send(ser,b"FX:\x0F")
read_ack(ser,"FX")
#time.sleep(0.1)
# focus near
send(ser,b"FN:")
read_ack(ser,"FN")
sleep(5)
send(ser,b"FS:")
read_ack(ser,"FS")
# focus far
delay = 1.0
if(len(sys.argv) > 1):
  try:
    delay = float(sys.argv[1])
  except ValueError:
    print "Couldn't parse float from {0}, using {1}".format(sys.argv[1],delay)
send(ser,b"FF:")
read_ack(ser,"FF")
sleep(delay)
send(ser,b"FS:")
read_ack(ser,"FS")
exit(0)
