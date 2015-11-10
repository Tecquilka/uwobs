#!/bin/sh
seconds="$1"
#/usr/local/bin/ffmpeg -t $seconds -f mpegts -i udp://226.0.0.1:1234 -vcodec copy -an -f segment  -segment_time 900 /home/dmuser/recordings/spiddal1-$(date +"%Y%m%d%H%M")-%03d.avi
/usr/local/bin/ffmpeg -i udp://226.0.0.1:1234 -t "$seconds" -vcodec copy -an -f segment  -segment_time 900 /home/dmuser/recordings/spiddal1-$(date +"%Y%m%d%H%M")-%03d.avi
