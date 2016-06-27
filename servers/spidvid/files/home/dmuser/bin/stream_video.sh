#!/bin/sh
mkdir -p /tmp/hls
start=$(date +%s)
/usr/local/bin/ffmpeg -f decklink \
                      -i "DeckLink Mini Recorder@13" \
                     -vf "drawtext=expansion=normal:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:reload=1:textfile=/home/dmuser/timenow.txt: x=10: y=690: fontcolor=white: fontsize=20" \
                       -codec:v libx264 -crf 18 -preset ultrafast\
                       -preset ultrafast \
                       -r 25 \
                       -pix_fmt yuv420p \
                       -an \
                       -f mpegts \
                       udp://226.0.0.1:1234
