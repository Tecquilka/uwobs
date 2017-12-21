#!/bin/sh
files_file=$(dirname $0)/../servers/$(hostname -s)/files.txt
if [ ! -e "$files_file" ]; then
  $(dirname $0)/backup_config.sh
fi

for file in "$@"
do
  if [ -e "$file" ]; then
    grep -q -F $file $files_file || echo $file | tee -a $files_file
  else
    echo "NOT FOUND: $file" >&2
  fi
done
$(dirname $0)/backup_config.sh
