#!/bin/sh
mkdir -p /tmp/hls
start=$(date +%s)
 /usr/local/bin/ffmpeg -i 'udp://226.0.0.1:1236' \
                       -vcodec copy -an \
                       -flags \
                       -global_header \
                       -hls_time 5 \
                       -hls_list_size 10 \
                       -hls_flags delete_segments \
                       -start_number $start \
                       -f hls \
                       /tmp/hls/spiddal1.m3u8
 #\
                       #-f flv \
                       #rtmp://127.0.0.1/dash/spiddal1 \
