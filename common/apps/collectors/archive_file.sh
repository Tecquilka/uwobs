#!/bin/sh
########################################
#
# Moves completed file to the Data folder
#
########################################
if [ "$2" = "" ]
then
  exit 0
fi
mv $2 $(dirname $2)/Data
