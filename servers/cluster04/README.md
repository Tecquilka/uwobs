# cluster04

[previous](../cluster03/) [next](../cluster05/)

This is the fourth of five nodes for cluster applications

address 172.17.1.95

user opsuser

## Services

  * HAProxy

## Docker

### Virtuoso

Virtuoso is running for evaluation by Adam.

Docker was started using the following command, and should restart automatically after reboot.

  docker run --name virtuoso -p 8890:8890 -p 1111:1111 -e SPARQL_UPDATE=true -e DEFAULT_GRAPH=http://virtuoso.dm.marine.ie/DAV -v /opt/virtuoso/db:/var/lib/virtuoso/db -d --restart=always tenforce/virtuoso


