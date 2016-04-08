#!/bin/sh
# old url was rtmp://193.1.189.55:1935/marine/marine
mkdir -p /tmp/hls
start=$(date +%s)
 /usr/local/bin/ffmpeg -i 'udp://226.0.0.1:1236' \
                       -vcodec libx264 \
                       -f flv \
                        "rtmp://transcode06.heanet.ie/35a780f500db4a28900a29119cd63da7?doConnect=TXGLOs0h"
