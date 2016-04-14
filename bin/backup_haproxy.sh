#!/bin/sh
SERVERS=$(readlink -f $(dirname $0)/../servers/)/cluster0*
for server in $SERVERS; do
   cp /etc/haproxy/haproxy.cfg $server/files/etc/haproxy/haproxy.cfg
done
