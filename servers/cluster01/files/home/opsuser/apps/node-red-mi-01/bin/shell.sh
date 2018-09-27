#!/bin/sh
. $(dirname $0)/../settings.sh || exit 1
docker exec -i -t $container /bin/bash
