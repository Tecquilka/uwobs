#!/usr/bin/env python
import sys
import socket
import fcntl, os
import errno
from time import sleep
from datetime import datetime

folder = '/home/gcouser/adcp'
device = "TRDI-WHB600Hz-1323"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('172.16.255.8',952))
fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)

chunks = []
nodata = True
f = None
filename = None
first_time = True

def next_filename():
    now = datetime.utcnow()
    return '{0}/{1}_{2}.pd0'.format(folder,device,now.strftime("%Y%m%d_%H%M"))


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
        nodata = False
    except socket.error, e:
        err = e.args[0]
        if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
            if f and nodata:
               f.close()
               f = None
               os.rename(filename+'.tmp',filename)
               if first_time or os.stat(filename).st_size < 211:
                   os.unlink(filename)
                   first_time = False
            nodata = True
            sleep(1)
            continue
        else:
            # a "real" error occurred
            print e
            sys.exit(1)
