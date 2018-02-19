#!/bin/sh
date
flock -n /tmp/rsync.spidvid-audio rsync -av --remove-source-files --include '*.wav' -e ssh 'dmuser@spidvid:/mnt/audio/ICListenRecordings/20*' /opt/data/spidvid/audio/ICListenRecordings/
