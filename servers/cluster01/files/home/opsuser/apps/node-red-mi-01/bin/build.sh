#!/bin/sh
cd $(dirname $0)/..
. ./settings.sh || exit 1
docker build -t $container .
