#!/bin/sh
cd $(dirname $0)/..
. ./settings.sh || exit 1
docker cp node-red-mi-01:/data/settings.js config/
docker cp node-red-mi-01:/data/.config.json config/config.json
docker cp node-red-mi-01:/data/flows.json config/
docker cp node-red-mi-01:/data/flows_cred.json config/
docker cp node-red-mi-01:/data/package.json config/
