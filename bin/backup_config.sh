#!/bin/sh
SERVER=$(hostname -s)
SERVERS_DIR=$(readlink -f $(dirname $0)/../servers/)/$SERVER
mkdir -p $SERVERS_DIR/files
FILES_LIST="$SERVERS_DIR/files.txt"
if [ ! -f "$FILES_LIST" ]; then
   cat >> "$FILES_LIST" << EOF
# list of files to be recorded
# prefix with a - any file to be excluded
# lines beginning with '#' will be ignored
/etc/network/interfaces
/etc/hosts
/etc/hostname
EOF
fi
for file in $(grep -v "^\s*\-" $FILES_LIST | grep -v "^\s*#") ; do
   TARGET=$(echo "$SERVERS_DIR/files/$file" | sed -e "s#//#/#g")
   TARGET_DIR=$(dirname "$TARGET")
   mkdir -p "$TARGET_DIR"
   echo copy $file to $TARGET >&2
   if [ -d "$file" ]; then
     cp -pr "$file" "$TARGET_DIR" || echo "Could not copy $file" >&2
   else
     cp -p $file "$TARGET" || echo "Could not copy $file" >&2
   fi
done
