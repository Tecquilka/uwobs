# cluster05

[previous](../cluster04/) [next](../data01/)

This is the fifth of five nodes for cluster applications

address 172.17.1.96

user opsuser

## Services

  * HAProxy

## Geonode

geonode is running in docker for evaluation by Trevor/Adam. The service should start automatically after system reboot and can be found at [geonode.dm.marine.ie](http://geonode.dm.marine.ie)

   docker run --name=geonode --restart=always -d -p 8111:8000 -p 8181:8080 geonode
