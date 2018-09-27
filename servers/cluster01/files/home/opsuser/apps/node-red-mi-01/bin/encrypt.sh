#!/bin/sh
docker run --rm nodered/node-red-docker node -e "console.log(require('bcryptjs').hashSync(process.argv[1], 8));" $1
