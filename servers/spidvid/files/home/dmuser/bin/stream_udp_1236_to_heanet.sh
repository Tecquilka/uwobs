#!/bin/sh
# old url was rtmp://193.1.189.55:1935/marine/marine
echo this job is moved to gconode02
exit 1
URL=$(cat /etc/heanet_video_url.txt)
mkdir -p /tmp/hls
start=$(date +%s)
 #/usr/local/bin/ffmpeg -i 'udp://226.0.0.1:1236?fifo_size=1000000&overrun_nonfatal=1' \
                       #-c:v copy -an \
/usr/local/bin/ffmpeg -i udp://226.0.0.1:1236 \
                       -vf "scale=640:-1" \
                       -r 25 \
                       -vcodec libx264 \
                       -an \
                       -f flv
                        $URL
