#!/usr/bin/python
# Rob Fuller, May 2017.
# For commands see:
# file://galwayfs03/Public/cabledObsManuals/Kongsberg-OE14-522-5100-rs232-commands.pdf
#
from serial import rfc2217,serial_for_url,Serial
from time import sleep, gmtime, strftime
import struct
from subprocess import call


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

send(ser,b"ST:")
response = read_ack(ser,"ST")
pos = response[3:]
print pos
positions = [
    {"pan":97,"tilt":220},{"pan":97,"tilt":236},{"pan":97,"tilt":245},
    {"pan":116,"tilt":239},{"pan":116,"tilt":229},{"pan":114,"tilt":223},
    {"pan":111,"tilt":220}
             ]
# above positions replaced Aug 8th 2017
positions = [
    {"pan":105,"tilt":150,"sleep": 6},
    {"pan":105,"tilt":130,"sleep": 2},
    {"pan":265,"tilt":150,"sleep": 8},
    {"pan":265,"tilt":130,"sleep": 2}
             ]



# Fast Zoom
#send(ser,b":ZX:"+b'\x0F')
#read_ack(ser,"ZX")
#time.sleep(0.1)
# Fast Focus
#send(ser,b":FX:"+b'\x0F')
#read_ack(ser,"FX")
#time.sleep(0.1)
# Fast Pan
#send(ser,b":DS:"+b'\x64')
#read_ack(ser,"DS")
#time.sleep(0.1)
# Fast Tilt
#send(ser,b":TA:"+b'\x64')
#read_ack(ser,"TA")
#time.sleep(0.1)
pan = positions[0]["pan"]
tilt = positions[0]["tilt"]
send(ser,b"GL:"+b"{0:0>3}".format(pan)+b"{0:0>3}".format(tilt))
read_ack(ser,"GL")
sleep(10)

# zoom wide
send(ser,b"ZW:")
read_ack(ser,"ZW")
sleep(3)
send(ser,b"ZS:")
read_ack(ser,"ZS")
# focus near
send(ser,b"FN:")
read_ack(ser,"FN")
sleep(10)
send(ser,b"FS:")
read_ack(ser,"FS")
# focus far
send(ser,b"FF:")
read_ack(ser,"FF")
sleep(4)
send(ser,b"FS:")
read_ack(ser,"FS")
# auto focus
#send(ser,b"PC:"+b'\x0C'+b'\x00'+b'\x00'+b'\x00')

folder = "/mnt/photo/spidvid/{0}".format(strftime("%Y/%m/%d",gmtime()))
call(["mkdir","-p",folder])

# stop the streaming
ffmpeg = ["/usr/local/bin/ffmpeg", "-f", "decklink","-i", "DeckLink Mini Recorder@13","-vf",
                     "drawtext=expansion=normal:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:reload=1:textfile=/home/dmuser/timenow.txt: x=10: y=690: fontcolor=white: fontsize=20"
                     ]
restart_streaming = False #True
# if call(["sudo", "supervisorctl", "stop", "ffmpeg_stream_from_device"]) != 0:
    # ffmpeg = ['/usr/local/bin/ffmpeg','-i','udp://226.0.0.1:1236']
    # restart_streaming = False
    
# TODO: take the photo now.
cmd = None
status = None
for position in positions:
  pan = position["pan"]
  tilt = position["tilt"]
  send(ser,b"GL:"+b"{0:0>3}".format(pan)+b"{0:0>3}".format(tilt))
  read_ack(ser,"GL")
  sleep(position["sleep"])

  for i in range(5):
    now = strftime("%Y-%m-%dT%H-%MZ", gmtime())
    file = "{0}/{1}_pan{2:0>3}_tilt{3:0>3}.jpg".format(folder,now,pan,tilt)
    cmd = ffmpeg + ['-vframes','1','-q:v','1','-y',file]
    #cmd = ffmpeg + ['-t','1','-f','image2',file]
    status = call(cmd,shell=False)
    if status:
        call(["rm","-f",file])
        #command failed. try again
        continue
    break
if restart_streaming:
    call(["sudo", "supervisorctl", "start", "ffmpeg_stream_from_device"])
    
#pos="180180"
send(ser,b"GL:"+pos)
read_ack(ser,"GL")
sleep(10)
# zoom wide
#send(ser,b"ZT:")
#read_ack(ser,"ZT")
#time.sleep(0.5)
#send(ser,b"ZS:")
#read_ack(ser,"ZS")
# focus far
#send(ser,b"FF:")
#read_ack(ser,"FF")
#time.sleep(0.5)
#send(ser,b"FS:")
#read_ack(ser,"FS")
# auto focus
#send(ser,b"PC:"+b'\x0C'+b'\x00'+b'\x00'+b'\x00')
#read_ack(ser,"FS")

if(status):
    print cmd
    print "The above command failed. Check the log"
    exit(status)
exit(0)

minpan = 90
maxpan = 270
mintilt = 90
maxtilt = 270
tilt = mintilt
pan = minpan
pandir = -1
while tilt <= maxtilt:
  pan = pan + pandir
  if pan < minpan or pan > maxpan:
     pandir = pandir * -1
     pan = pan + pandir + pandir
     tilt += 20
  send(ser,b"GL:"+b"{0:0>3}".format(pan)+b"{0:0>3}".format(tilt))
  sleep(0.1)
#Go back to the original position.
send(ser,b"GL:"+pos)
#time.sleep(1)
#send(ser,b"PL:")
#time.sleep(12)
#send(ser,b"PS:")
#time.sleep(0.1)
#send(ser,b"PP:120")
#time.sleep(5)
#send(ser,b"PP:120")
#send(ser,b"ST:")
