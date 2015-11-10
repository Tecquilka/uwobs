#!/usr/bin/env python
from daytimes import *
from local_info import lat, lon, delta_minutes
import subprocess


def stream_rtmp_video(fro,seconds):
    command = ["/usr/local/bin/ffmpeg", "-i", fro, "-t", str(seconds), "-c:v", "copy", "-acodec", "copy", "-f", "flv", "rtmp://marine:12eB7za7S79d@193.1.189.55:1935/marine"]
    print "streaming {0} to heanet for {1} seconds".format(fro,seconds)
    print command
    subprocess.call(command)

while True:
    daytime = is_it_daytime(lat,lon,delta_minutes)
    if(daytime):
        stream_rtmp_video(fro="udp://226.0.0.1:1234",seconds=seconds_till_daytime_ends(lat,lon,delta_minutes))
    else:
        stream_rtmp_video(fro="udp://226.0.0.1:1235",seconds=seconds_till_daytime(lat,lon,delta_minutes))

