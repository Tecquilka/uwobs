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

CONFIG=$(dirname $0)/configure_adcp.py
export $($CONFIG | grep -v '^#' | xargs)
HTTP_PORT=8085
PYTHON=$HOME/virtualenv/serial2kafka/bin/python
COLLECT_ADCP=$(dirname $0)/../catserial/collect_adcp.py


$PYTHON $COLLECT_ADCP --server "$SERVER" --port "$PORT" --source "$SOURCE" --http-port $HTTP_PORT

status=$?
while [ $SECONDS -lt 26 ]; do
    echo -n . >&2
    sleep 1
done
sleep 5
echo "done" $(date) >&2
exit $status
