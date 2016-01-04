#!/bin/bash
##################################################
#
# This script fetches lines of csv from a website
# and puts each line as a message on a kafka queue
#
##################################################
. /etc/mestech.conf || ( echo /etc/mestech.conf not found >&2 && exit 1 )

data_dir=/data/mestech/$instrument_id/$today_path
state_dir=~/.mestech/state
state_file=$state_dir/$instrument_id.txt
today_path=$(date '+%Y/%m/%d')
data_file=$data_dir/${instrument_id}_$(date '+%Y%m%d').txt
mkdir -p $state_dir || exit 1
mkdir -p $data_dir || exit 1
# Read start date from file, or generate one.
start_date=$(head -1 $state_file | grep -e '^../../2....2...:..:..$')
if [ "$start_date" == "" ]; then
  start_date=$(date -d "yesterday 00:01" '+%d/%m/%Y')"%2000:00:01"
fi
end_date=$(date -d "tomorrow 00:01" '+%d/%m/%Y')"%2023:59:59"
# construct the URL using the site id and start_date.
URL="${url}&start=${start_date}&end=${end_date}"
# Fetch the URL and append any new lines to kafka
# grab the new start time from the final line.
# We ignore the first two lines: the header and first data line.
http_proxy=http://10.0.5.55:80 curl -s $URL \
                               | tail -n +3 \
                               | tee >( tail -1 | awk -F , '{print $1 "%20" $2}' > $state_file.new) \
                               | tee -a $data_file \
                               | /usr/local/bin/kafkacat  -P -b kafka01 -t $instrument_id -p 0

status=$?
if [ "$status" == "0" ] && [ -s $state_file.new ]; then
  # write new start date to the file for next time round.
  mv $state_file.new $state_file
else
  rm $state_file.new
fi

exit $status
