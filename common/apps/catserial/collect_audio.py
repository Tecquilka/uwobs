#!/usr/bin/env python
import sys
import socket
import fcntl, os
import errno
import datetime
import argparse
from midas import WebServer, KillerMonitor, is_number
from time import time as now, sleep
from struct import pack, unpack
import io
# import wave #NO, not using this.
import atexit
import time


parser = argparse.ArgumentParser(description='collect icListen waveform data into a file')
parser.add_argument('--server', required=True, help='icListen server ip address to connect to')
parser.add_argument('--port', default=51678, type=int, help='icListen port to connect to (default is 51678)')
parser.add_argument('--timeout', type=int, default=120, help='Number of seconds to wait for messages before giving up, default=120 (2 minutes)')
parser.add_argument('--http-port', type=int, default=8196, help='HTTP web server port showing latest message, default is 8196')
args = parser.parse_args()

folder = '/mnt/audio/ICListenRecordings'

killer = KillerMonitor(args.timeout)
killer.setDaemon(True)
killer.start()
sys.stderr.write("Monitoring icListen %s:%d will kill application if unable to process a message for %d seconds\n" % (args.server, args.port, args.timeout))

webserver = WebServer(args.http_port)
webserver.setDaemon(True)
webserver.start()
sys.stderr.write("Web server running on port %d\n" % args.http_port)

serial_number = None
def get_next_filename(folder):
  utc_datetime = datetime.datetime.utcnow()
  dirname = "{0}/{1}".format(folder,utc_datetime.strftime("%Y/%m/%d"))
  try:
    os.makedirs(dirname)
  except OSError as exc: 
    if not (exc.errno == errno.EEXIST and os.path.isdir(dirname)):
      raise
  return "{0}/icListen_{1}_{2}.wav".format(dirname,serial_number,utc_datetime.strftime("%Y%m%dT%H%M%SZ"))


NOTIFY = '0'
DATA = '1'
EVENT_HEADER = '2'
START_STREAM = '3'
STOP_STREAM = '4'

EVENT_KEY_CHUNK = 'A'
DATA_CHUNK = 'B'
STATUS_CHUNK = 'C'
DEVICE_INFO_CHUNK = 'D'
WAVE_SETUP_CHUNK = 'E'
SPECTRUM_SETUP_CHUNK = 'F'
AMPLITUDE_SCALING_CHUNK = 'G'
TEMERATURE_HUMIDITY_CHUNK = 'H'
HEADING_CHUNK = 'I'
TIME_SYNC_CHUNK = 'J'
BATTERY_CHUNK = 'K'
TRIGGER_STATUS_CHUNK = 'L'



def process_chunk(stream):
   (chunk_type,
    version,
    chunk_size,) = unpack('!cBH',chunkstream.read(4))
   data = stream.read(chunk_size)
   

def handle_notify(payload):
   code = unpack('!i',payload)[0]
   codes = [
           'undefined',
           'No Free Connection',
           'Timeout',
           'Stream Stopped',
           'Invalid Start Message',
           'Logging Active',
          ]
   print codes[code]

big_endian = '>'
little_endian = '<'
bytes_per_sample = None
num_channels = 0
def handle_data_chunk(version,stream):
     global num_channels
     (sample_num,
     num_channels,
     data_format,
     num_samples) = unpack('!IBbH',stream.read(8))
     endian = big_endian
     if data_format < 0:
        endian = little_endian
     data_size = num_samples * bytes_per_sample * num_channels
     data = stream.read(data_size)
     global samples
     samples.extend(data)
     # print 'sample {0} numchannels {1} left {2} wanted {3} got {4}'.format(sample_num,num_channels,len(stream.read(4096)),data_size,len(data))
    
def handle_event_key_chunk(version,stream):
    (unix_time,
     seq_num_high,
     seq_num_low) = unpack('!III',stream.read(12))
    # print "event_key_chunk unix_time={0}, seq_num_low={1}, seq_num_high={2}".format(unix_time,seq_num_low,seq_num_high)

def handle_status_chunk(version,stream):
    (temperature,
     humidity,
     battery_charge,
     battery_status,
     data_epoch,
     channel_num) = unpack('!HHBBBB',stream.read(8))
    reserved = stream.read(12)
    # print "temperature: {0}, humidity: {1}".format(temperature/10.0, humidity/10.0)

def handle_data(payload):
   # print "data_chunk"
   chunkstream = io.BytesIO(payload)
   header = chunkstream.read(4)
   while len(header) == 4:
     (chunk_type,
      version,
      chunk_size,) = unpack('!cBH',header)
     # print "chunk_size for type {0} is {1}".format(chunk_type,chunk_size)
     chunk = chunkstream.read(chunk_size)
     if len(chunk) == 0: 
        return # why????
     if len(chunk) != chunk_size:
        print "expected {0} but got {1}".format(chunk_size,len(chunk))
     
     handler = None
     try:
       handler = chunk_handlers[chunk_type]
     except KeyError:
       print "no chunk handler configured for chunk_type={0}".format(chunk_type)
     if handler:
        handler(version,io.BytesIO(chunk))

     header = chunkstream.read(4)

def handle_event_header(payload):
    # print "event_header"
    # print "****************event_header****************"
    handle_data(payload)

def handle_device_info_chunk(version,stream):
    global serial_number, fname
    (model,
    firmware_version,
    serial_number,
    phone_sensitivity) = unpack('!B3sHH',stream.read(8))
    # print "device", firmware_version,serial_number
    if fname is None:
      fname = get_next_filename(folder)

samples = []
fname = None
sample_rate = None
def handle_wave_setup_chunk(version,stream):
    global sample_rate
    (sample_rate,
     gain,
     data_format,
     reserved) = unpack('!IHbB',stream.read(8))
    endian = 'small'
    if data_format < 0:
       endian = 'big'
    xbytes_per_sample = abs(data_format)
    # print "wave setup: sample_rate={0}, gain={1}, endian={2}, bytes_per_sample={3} now have {4} bytes".format(sample_rate,gain,endian,xbytes_per_sample,len(samples))
    # if len(samples):
    if len(samples) and len(samples) >= 60 * bytes_per_sample * sample_rate * num_channels:
      # print "writing {0} bytes".format(len(samples))
      writewav()

def handle_spectrum_setup_chunk(version,stream):
    # print "spectrum setup chunk"
    pass

def handle_amplitude_scaling_chunk(version,stream):
    global bytes_per_sample, samples
    (channel_num,
     unit_of_measure,
     reserved,
     bytes_per_sample,
     max_count,
     min_count,
     max_amplitude,
     min_amplitude) = unpack('!BBBBIIII',stream.read(20))
    # print "channel {0} bytes_per_sample: {1} uom={2} counts({3},{4}) amplitude({5},{6})".format(channel_num,bytes_per_sample,unit_of_measure,min_count,max_count,min_amplitude,max_amplitude) 
    # print time.strftime("%H:%M:%S");

message_handlers = {
  NOTIFY: handle_notify,
  DATA: handle_data,
  EVENT_HEADER: handle_event_header
}

chunk_handlers = {
  EVENT_KEY_CHUNK: handle_event_key_chunk,
  DATA_CHUNK: handle_data_chunk,
  STATUS_CHUNK: handle_status_chunk,
  DEVICE_INFO_CHUNK: handle_device_info_chunk,
  WAVE_SETUP_CHUNK: handle_wave_setup_chunk,
  SPECTRUM_SETUP_CHUNK: handle_spectrum_setup_chunk,
  AMPLITUDE_SCALING_CHUNK: handle_amplitude_scaling_chunk,
}

def writewav():
  global bytes_per_sample, sample_rate, num_channels, samples, fname
  if not len(samples):
    return
  nchannels = num_channels
  sampwidth = bytes_per_sample # n bytes per sample
  framerate = sample_rate # sampling rate
  byterate = framerate * nchannels * sampwidth 
  blockalign = nchannels * sampwidth

  # read PCM data
  with open(fname, 'wb') as wavfile:
    pcm_size = len(samples)
    chunk_size = pcm_size + 36
    # convert PCM to wav, all we need is just a header
    wav = ''
    wav += pack('>cccc', 'R','I','F','F') # ChunkID, contains the
                                          # letters "RIFF" in ASCII
                                          # form(0x52494646 big-endian)
    wav += pack('<I', chunk_size) # ChunkSize, this is the size of the
                                  # rest of the chunk following this number

    wav += pack('>cccc', 'W','A','V','E') # Format, contains the
                                          # letters "WAVE"(0x57415645 big-endian)

#--------------------------------------------------------------------
    wav += pack('>cccc', 'f','m','t',' ') # Subchunk1ID, contains the 
                                          # letters "fmt "(0x666d7420 big-endian)
    wav += pack('<I', 16) # Subchunk1ISize, 16 for PCM
    wav += pack('<H', 1) # AudioFormat, PCM = 1, values other than 1 indicate some form of compression
    wav += pack('<H', nchannels) # NumChannels, mono = 1, stereo = 2, etc
    wav += pack('<I', framerate) # 8000, 44100, etc
    wav += pack('<I', byterate) # samplerate * numchannels * bitspersample / 8
    wav += pack('<H', blockalign) # numchannels * bitspersample / 8
    wav += pack('<H', sampwidth * 8) # bitspersample

#--------------------------------------------------------------------
    wav += pack('>cccc','d','a','t','a') # Subchunk2ID, contains the letters "data"(0x64617461 big-endian)
    wav += pack('<I', pcm_size) # number of bytes in the data
    wavfile.write(wav)
    wavfile.write(bytearray(samples))
  samples = []
  fname = get_next_filename(folder)

atexit.register(writewav)


s = socket.socket()
s.connect((args.server, args.port))
s.send(bytearray(b'\x33\x2a\x00\x04\x00\x00\x00\x00'))
while True:
  data = s.recv(2)
  if(len(data) == 0):
    break
  (msg_char, sync,) = unpack('!cB',data)
  if sync != 0x2A:
    print "wrong sync"
  else:
    data = s.recv(2, socket.MSG_WAITALL)
    (payload_length,) = unpack('!H',data)
    payload = s.recv(payload_length, socket.MSG_WAITALL)
    handler = None
    try:
      handler = message_handlers[msg_char]
      killer.ping()
      webserver.update("(binary)")
    except KeyError:
      print "no handler configured for msg_char={0}".format(msg_char)
    if handler:
      handler(payload)

s.close();
