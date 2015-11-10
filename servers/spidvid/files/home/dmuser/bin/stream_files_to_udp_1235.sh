#!/bin/sh
while [ 1 ] ; do
 for avi in /home/dmuser/recordings/*.avi
 do
  #ffmpeg -re -i $avi -c:v copy -an -f mpegts udp://226.0.0.1:1235
  ffmpeg -re -i $avi -vcodec libx264 -an -f mpegts udp://226.0.0.1:1235
 done
done
