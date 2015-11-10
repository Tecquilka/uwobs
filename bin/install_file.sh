#!/bin/sh
#######################################
#
# copies a file for this server to the target location
# eg: bin/install_file.sh /etc/hosts
#
######################################
SERVER=$(hostname -s)
SERVERS_DIR=$(readlink -f $(dirname $0)/../servers/)/$SERVER
file=$1
if [ ! -f "$file" ]; then
   echo not a file: $file >&2
   exit 2
fi
source=$(readlink -f "$SERVERS_DIR/files/$file")
if [ ! -f "$source" ]; then
   echo not a file: $source >&2
   exit 2
fi
echo copy $source $file >&2
cp -p $source $file
