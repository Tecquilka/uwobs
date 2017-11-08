#!/bin/bash
##################################################################
#
# Writes icListen wav to files
#
# icListen code developed under NDA, so the collector is not
# available in github.
#
# Script is executed by supervisor,
# see /etc/supervisor/conf.d/icListen.conf
################################################################## 
while [ $(cat /proc/uptime | awk '{print $1}' | sed 's/\..*$//') -lt 180 ]
do 
   echo waiting for 3 minutes of uptime... >&2 
   sleep 10
done

SERVER=172.16.255.254
HTTP_PORT=8196
COLLECT_WAV=$HOME/dev/uwobs/common/apps/catserial/collect_audio.py


$COLLECT_WAV --server "$SERVER" --http-port $HTTP_PORT

status=$?
while [ $SECONDS -lt 31 ]; do
    echo -n . >&2
    sleep 1
done
echo "done" $(date) >&2
exit $status
