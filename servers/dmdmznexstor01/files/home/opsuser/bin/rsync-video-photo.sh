#!/bin/sh
date
flock -n /tmp/rsync.spidvid rsync -av --remove-source-files --include '*.mp4' -e ssh 'dmuser@spidvid:/mnt/video/aja-helo-1H000314/20*' /opt/data/spidvid/video/aja-helo-1H000314/
flock -n /tmp/rsync.spidvid rsync -av --remove-source-files --include '*.jpg' -e ssh 'dmuser@spidvid:/mnt/photo/spidvid/20*' /opt/data/spidvid/photo/spidvid/
#rsync -av --remove-source-files --include '*.wav' -e ssh 'dmuser@spidvid:/mnt/audio/ICListenRecordings/20*' /opt/data/spidvid/audio/ICListenRecordings/
