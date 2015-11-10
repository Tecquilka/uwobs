#!/usr/bin/env python
from daytimes import *
from local_info import lat, lon, delta_minutes
import subprocess
import time

while True:
    daytime = is_it_daytime(lat,lon,delta_minutes)
    if daytime:
        seconds=seconds_till_daytime_ends(lat,lon,delta_minutes)
        print "recording for {0} seconds".format(seconds)
        command = ['/home/dmuser/bin/record_stream.sh', str(seconds)]
        subprocess.call(command)
    else:
        seconds=seconds_till_daytime(lat,lon,delta_minutes)
        print "sleeping for {0} seconds".format(seconds)
        time.sleep(seconds)

