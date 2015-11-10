#!/usr/bin/env python
from daytimes import *
from local_info import lat, lon, delta_minutes
import subprocess


def stream_udp_video(fro,to,seconds):
    command = ["/usr/local/bin/ffmpeg", "-i", fro, "-t", str(seconds), "-c:v", "copy", "-an", "-f", "mpegts", to]
    print "streaming {0} to {1} for {2} seconds".format(fro,to,seconds)
    print command
    subprocess.call(command)

while True:
    daytime = is_it_daytime(lat,lon,delta_minutes)
    if(daytime):
        stream_udp_video(fro="udp://226.0.0.1:1234",to="udp://226.0.0.1:1236",seconds=seconds_till_daytime_ends(lat,lon,delta_minutes))
    else:
        stream_udp_video(fro="udp://226.0.0.1:1235",to="udp://226.0.0.1:1236",seconds=seconds_till_daytime(lat,lon,delta_minutes))

