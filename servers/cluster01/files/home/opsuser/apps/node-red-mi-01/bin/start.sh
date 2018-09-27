#!/bin/sh
. $(dirname $0)/../settings.sh || exit 1
docker run -p $ports -d --restart=always --name=$container --add-host=kafka01:172.17.1.86 --add-host=kafka02:172.17.1.87 --add-host=kafka03:172.17.1.88 $container
