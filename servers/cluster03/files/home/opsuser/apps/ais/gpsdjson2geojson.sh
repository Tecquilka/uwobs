#!/bin/bash
##################################################################
#
# converts ais gpsd json to geojson
#
# see /etc/superviser/conf.d/apps-supervisor.conf
#
################################################################## 
PYTHON=/home/opsuser/virtualenvs/ais/bin/python
SCRIPT=/home/opsuser/apps/ais/gpsdjson2geojson.py


$PYTHON $SCRIPT  --consume ais-rinville-1-gpsdjson --publish ais-rinville-1-geojson

status=$?
while [ $SECONDS -lt 31 ]; do
    echo -n . >&2
    sleep 1
done
echo "done" $(date) >&2
exit $status
