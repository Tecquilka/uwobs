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
while [ $(cat /proc/uptime | awk '{print $1}' | sed 's/\..*$//') -lt 120 ]
do 
   echo waiting for 2 minutes of uptime... >&2 
   sleep 10
done

SOURCE=TRDI-WHB600Hz-1323
PORT=952
SERVER=172.16.255.8
HTTP_PORT=8085
PYTHON=/home/gcouser/virtualenv/serial2kafka/bin/python
COLLECT_ADCP=/home/gcouser/apps/catserial/collect_adcp.py


$PYTHON $COLLECT_ADCP --server "$SERVER" --port "$PORT" --source "$SOURCE" --http-port $HTTP_PORT

status=$?
while [ $SECONDS -lt 31 ]; do
    echo -n . >&2
    sleep 1
done
echo "done" $(date) >&2
exit $status
