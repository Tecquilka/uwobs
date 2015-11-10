#!/bin/sh
mkdir -p /tmp/hls
start=$(date +%s)
 /usr/local/bin/ffmpeg -i 'udp://226.0.0.1:1236' \
                       -vcodec libx264 \
                       -f flv \
                       rtmp://193.1.189.55:1935/marine/marine
