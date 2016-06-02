#!/bin/bash
##################################################################
#
# converts ais data to json
#
# see /etc/superviser/conf.d/apps-supervisor.conf
#
################################################################## 
PYTHON=/home/opsuser/virtualenvs/ais/bin/python
SCRIPT=/home/opsuser/apps/ais/ais2gpsdjson.py


$PYTHON $SCRIPT 

status=$?
while [ $SECONDS -lt 31 ]; do
    echo -n . >&2
    sleep 1
done
echo "done" $(date) >&2
exit $status
