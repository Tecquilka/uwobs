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

CONFIG=$(dirname $0)/configure_hydrophone.py
export $( https_proxy=http://172.16.255.226:3128 $CONFIG | grep -v '^#' | xargs)
HTTP_PORT=8196
COLLECT_WAV=$HOME/dev/uwobs/common/apps/catserial/collect_audio.py

# call the reset command on the hydrophone
echo calling reset on the hydrophone
curl --max-time 10 -s "http://${SERVER}/cgi-bin/Operation.cgi?data=%7B%22action%22%3A%22reset%22%2C%22newtime%22%3A$(date +%s)%7D"

echo waiting for 60 seconds before connecting to hydrophone audio stream
sleep 60

$COLLECT_WAV --server "$SERVER" --http-port $HTTP_PORT

status=$?
while [ $SECONDS -lt 31 ]; do
    echo -n . >&2
    sleep 1
done
echo "done" $(date) >&2
exit $status
