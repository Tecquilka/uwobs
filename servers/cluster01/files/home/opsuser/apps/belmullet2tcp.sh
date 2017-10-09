#!/bin/bash
##################################################################
#
# Publishes kafka stream to a tcp socket server
#
# Script is executed by supervisor,
# see /etc/superviser/conf.d/apps-supervisor.conf
#
################################################################## 

nc6 --continuous -l -p 9987 -e 'stdbuf -oL kafkacat -C -b kafka01 -t ais-belmullet-json -p 0 -o -1'

status=$?
while [ $SECONDS -lt 31 ]; do
    echo -n . >&2
    sleep 1
done
echo "done" $(date) >&2
exit $status
