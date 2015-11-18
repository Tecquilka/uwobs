#!/usr/bin/env python
# author: fullergalway 
# date: 2015-04-30
from serial import rfc2217,serial_for_url,Serial
#from serial import rfc2217
import datetime
import argparse
import os
import sys
from midas import WebServer, KillerMonitor, is_number
from time import time as now, sleep

parser = argparse.ArgumentParser(description='Print timestamped lines from a serial device.')
parser.add_argument('--device', required=True, help='Url of the device, eg: rfc2217://10.11.104.3:7000')
parser.add_argument('--source', required=True, help='Name or id of the source to be included in the output')
parser.add_argument('--baud', type=int, default=9600, help='The baud rate')
parser.add_argument('--separator', default="|", help='The separator')
parser.add_argument('--timeout', type=int, default=300, help='Number of seconds to wait for messages before giving up, default=300 (5 minutes)')
parser.add_argument('--http-port', type=int, default=8082, help='HTTP web server port showing latest message, default is 8082')
args = parser.parse_args()

if "rfc2217://" in args.device:
  ser = rfc2217.Serial(args.device,args.baud,timeout=args.timeout)
elif "://" in args.device:
  ser = serial_for_url(args.device,baudrate=args.baud,timeout=args.timeout)
else:
  ser = Serial(args.device,baudrate=args.baud,timeout=args.timeout)

killer = KillerMonitor(args.timeout)
killer.setDaemon(True)
killer.start()
sys.stderr.write("Monitoring %s will kill application if unable to process a message for %d seconds\n" % (args.device, args.timeout))

webserver = WebServer(args.http_port)
webserver.setDaemon(True)
webserver.start()
sys.stderr.write("Web server running on port %d\n" % args.http_port)

while 1:
    line = ser.readline().rstrip()
    if line:
      timestamp = datetime.datetime.utcnow().isoformat()[:-3]+"Z"
      output = u"{1}{0}{2}{0}{3}".format(args.separator,timestamp,args.source,line)
      print output
      sys.stdout.flush()
      killer.ping()
      webserver.update(output)
