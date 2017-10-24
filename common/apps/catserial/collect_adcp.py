#!/usr/bin/env python
import sys
import socket
import fcntl, os
import errno
from time import sleep
import datetime
import argparse
from midas import WebServer, KillerMonitor, is_number
from time import time as now, sleep
import subprocess

parser = argparse.ArgumentParser(description='collect adcp data into a file')
parser.add_argument('--server', required=True, help='adcp server ip address to connect to')
parser.add_argument('--port', required=True, type=int, help='adcp port to connect to')
parser.add_argument('--source', required=True, help='Name or id of the source to be included in the output')
parser.add_argument('--timeout', type=int, default=1200, help='Number of seconds to wait for messages before giving up, default=1200 (20 minutes)')
parser.add_argument('--http-port', type=int, default=8085, help='HTTP web server port showing latest message, default is 8085')
parser.add_argument('--kafka-server', default='localhost', help='kafka server, default is localhost')
parser.add_argument('--kafka-topic', default='spiddal-adcp', help='kafka topic, default is spiddal-adcp')
parser.add_argument('--kafkacat', default='/usr/local/bin/kafkacat', help='path to kafkacat')
args = parser.parse_args()

folder = '/home/gcouser/adcp'
device = args.source

killer = KillerMonitor(args.timeout)
killer.setDaemon(True)
killer.start()
sys.stderr.write("Monitoring %s:%d will kill application if unable to process a message for %d seconds\n" % (args.server, args.port, args.timeout))

webserver = WebServer(args.http_port)
webserver.setDaemon(True)
webserver.start()
sys.stderr.write("Web server running on port %d\n" % args.http_port)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((args.server,args.port))
fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)

chunks = []
nodata = True
f = None
filename = None
first_time = True

def file_path_for_timestamp(timestamp):
    return '{0}/{1}_{2}.pd0'.format(folder,device,timestamp.strftime("%Y%m%d_%H%M"))
def next_filename():
    now = datetime.datetime.utcnow()
    delta = datetime.timedelta(seconds=30)
    path = file_path_for_timestamp(now - delta)
    if first_time or os.path.isfile(path):
       path = file_path_for_timestamp(now)
       if os.path.isfile(path):
          path = file_path_for_timestamp(now + delta)
    return path


def write_to_file(b):
    global f
    global filename
    if not f:
        filename = next_filename()
        f = open(filename+'.tmp', 'wb')
    f.write(b)

while True:
    try:
        write_to_file(s.recv(4096))
        killer.ping()
        webserver.update("(binary)")
        nodata = False
    except socket.error, e:
        err = e.args[0]
        if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
            if f and nodata and next_filename() != filename:
               f.close()
               f = None
               os.rename(filename+'.tmp',filename)
               if first_time or os.stat(filename).st_size < 211:
                   os.unlink(filename)
                   first_time = False
               else:
                   try:
                       subprocess.call( [args.kafkacat, '-P', '-b', args.kafka_server, '-t',
                                    args.kafka_topic, '-p', '0', filename])
                   except Exception, e:
                       print >> sys.stderr, 'problem writing to kafka: %s' % e

            nodata = True
            sleep(0.01)
            continue
        else:
            # a "real" error occurred
            print e
            sys.exit(1)
