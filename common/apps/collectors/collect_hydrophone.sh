#!/bin/bash
##################################################################
#
# Collect files from hydrophone using rsync and append to kafka
#
# Script is executed by cron
################################################################## 


CONFIG=$(dirname $0)/configure_hydrophone.py
export $($CONFIG | grep -v '^#' | xargs)
TYPE=hydrophone
DATA_DIR=/home/gcouser/$TYPE/
REMOTE_USER=icListen
REMOTE_FOLDER=Data
REMOTE_LOCATION="${REMOTE_USER}@${SERVER}:${REMOTE_FOLDER}"
KAFKA_SERVER=localhost
KAFKA_TOPIC=spiddal-$TYPE
KAFKACAT=/usr/local/bin/kafkacat

log=$(flock -n /tmp/${TYPE}.lock -c "rsync -iavz --timeout=30 --remove-source-files -e ssh --rsync-path bin/rsync ${REMOTE_LOCATION} $DATA_DIR") || exit $?
newFiles=$(echo "$log" | grep '>f+++++++++' | cut -d' ' -f2)
if [ -z "$newFiles" ]; then
  exit 0;
fi

for file in $(echo "$newFiles"); do
  # echo collected $file
  $KAFKACAT -P -b "$KAFKA_SERVER" -t "$KAFKA_TOPIC" -p 0 "${DATA_DIR}/$file" || exit $?
done

