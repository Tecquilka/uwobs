#!/usr/bin/env python
from time import sleep, gmtime, strftime
logfile = '/home/dmuser/timenow.txt'
f = open(logfile, 'r+')
while True:
    sleep(0.1)
    f.seek(0)
    f.write(strftime("%Y-%m-%dT%H:%M:%SZ (UTC)", gmtime()))
    f.flush()
f.close()
