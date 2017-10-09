#!/bin/bash
##################################################################
#
# Publishes kafka stream to a tcp socket server
#
# Script is executed by supervisor,
# see /etc/superviser/conf.d/apps-supervisor.conf
#
################################################################## 

stdbuf -oL kafkacat -C -b kafka01 -t ais-belmullet-json -p 0 -o -1 |  netcat -l 9987 -k

status=$?
while [ $SECONDS -lt 31 ]; do
    echo -n . >&2
    sleep 1
done
echo "done" $(date) >&2
exit $status
