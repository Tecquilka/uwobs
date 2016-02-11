#!/bin/bash
##################################################################
#
# Writes data from a socket to a file, rotating the file each minute
#
# Log rotation is done using rotatelogs from apache-utils package
#
# Script is executed by supervisor,
# see /etc/supervisor/conf.d/ctd.conf
################################################################## 
while [ $(cat /proc/uptime | awk '{print $1}' | sed 's/\..*$//') -lt 180 ]
do 
   echo waiting for 3 minutes of uptime... >&2 
   sleep 10
done


TYPE=acoustic_telemetry
DEVICE=VMVR2C450117
PORT=950
DATA_DIR=$HOME/$TYPE
SERVER=172.16.255.8
ARCHIVER=$(dirname $0)/archive_file.sh
HTTP_PORT=8084
KAFKA_SERVER=localhost
KAFKA_TOPIC=spiddal-$TYPE
PYTHON=$HOME/virtualenv/serial2kafka/bin/python
CATSERIAL=$(dirname $0)/../catserial/catserial.py

mkdir -p $DATA_DIR || exit 1
mkdir -p $DATA_DIR/Data || exit 1

$PYTHON $CATSERIAL --device "socket://$SERVER:$PORT" --source "$DEVICE" --http-port $HTTP_PORT \
                   | tee >( kafkacat -P -b "$KAFKA_SERVER" -t "$KAFKA_TOPIC" -p 0 ) \
                   | rotatelogs -p $ARCHIVER "$DATA_DIR/${DEVICE}_%Y%m%d_%H%M.txt" 60

status=$?
while [ $SECONDS -lt 31 ]; do
    echo -n . >&2
    sleep 1
done
echo "done" $(date) >&2
exit $status
