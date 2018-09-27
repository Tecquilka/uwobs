#!/bin/sh
cd $(dirname $0)/..
. ./settings.sh || exit 1
docker stop $container || exit 1
docker rm $container
