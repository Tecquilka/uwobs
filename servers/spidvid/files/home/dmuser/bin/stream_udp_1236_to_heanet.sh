#!/bin/sh
mkdir -p /tmp/hls
start=$(date +%s)
 /usr/local/bin/ffmpeg -i 'udp://226.0.0.1:1236' \
                       -vcodec libx264 \
                       -f flv \
                       rtmp://193.1.189.55:1935/marine/marine
                       #rtmp://193.1.189.55:1935/marine
                       #rtmp://193.1.189.55:1935/marine/spidvid
                       #rtmp://marine:12eB7za7S79d@193.1.189.55:1935/marine
                       # rtmp://193.1.189.55:1935/marine
