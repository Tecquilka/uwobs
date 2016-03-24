#!/bin/bash
##################################################################
#
# Collect files from hydrophone using rsync and append to kafka
#
# Script is executed by cron
################################################################## 


TYPE=hydrophone
DATA_DIR=$HOME/$TYPE/
SERVER=172.16.255.253
REMOTE_USER=icListen
REMOTE_FOLDER=Data
REMOTE_LOCATION="${REMOTE_USER}@${SERVER}:${REMOTE_FOLDER}"
KAFKA_SERVER=localhost
KAFKA_TOPIC=spiddal-$TYPE
CATSERIAL=/home/gcouser/apps/catserial/catserial.py

log=$(flock -n /tmp/${TYPE}.lock -c "rsync -iavz --remove-source-files -e ssh --rsync-path bin/rsync ${REMOTE_LOCATION} $DATA_DIR") || exit $?
newFiles=$(echo "$log" | grep '>f+++++++++' | cut -d' ' -f2)
if [ -z "$newFiles" ]; then
  exit 0;
fi

for file in $(echo "$newFiles"); do
  echo collected $file
  kafkacat -P -b "$KAFKA_SERVER" -t "$KAFKA_TOPIC" -p 0 "${DATA_DIR}/$file" || exit $?
done

