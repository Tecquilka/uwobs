# cluster03

[previous](../cluster02/) [next](../cluster04/)

This is the third of five nodes for cluster applications

address 172.17.1.94

user opsuser

## Services

  * HAProxy
  * mestech data collector
  * geonetwork (evaluation)

## Docker

geonetwork running for evaluation by Trevor/Adam must be restarted manually after a reboot using the following commands.

  docker start geonetwork_postgis
  docker start geonetwork

The service should become available at: [geonetwork.dm.marine.ie](http://geonetwork.dm.marine.ie)

