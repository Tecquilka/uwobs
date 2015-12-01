#!/bin/bash
##################################################################
#
# Writes data from a kafka to cassandra
#
# Script is executed by supervisor,
# see /etc/superviser/conf.d/apps-supervisor.conf
#
################################################################## 
PYTHON=/home/opsuser/virtualenvs/kafka2cassandra/bin/python
SCRIPT=/home/opsuser/apps/kafka2cassandra/ctd2cassandra.py

$PYTHON $SCRIPT
status=$?
while [ $SECONDS -lt 31 ]; do
    echo -n . >&2
    sleep 1
done
echo "done" $(date) >&2
exit $status
