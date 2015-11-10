#!/bin/sh
##################################################################
#
# Writes data from a socket to a file, rotating the file each minute
#
# Log rotation is done using rotatelogs from apache-utils package
#
# Script is executed by supervisor,
# see /etc/supervisor/conf.d/vemco.conf
################################################################## 
TYPE=acoustic_telemetry
DEVICE=VMVR2C450117
PORT=950
DATA_DIR=$HOME/$TYPE
SERVER=172.16.255.8
ARCHIVER=$(dirname $0)/archive_file.sh
TIMESTAMPER=$(dirname $0)/add_timestamp_and_id.py

mkdir -p $DATA_DIR || exit 1
mkdir -p $DATA_DIR/Data || exit 1

nc -w 600 $SERVER $PORT |stdbuf -o0 sed -e 's/\r//' | stdbuf -o0 grep -E \[0-9\] | stdbuf -oL $TIMESTAMPER "$DEVICE" |rotatelogs -p $ARCHIVER "$DATA_DIR/${DEVICE}_%Y%m%d_%H%M.txt" 60

status=$?
sleep 10
exit $status
