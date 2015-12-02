# cluster01

previous [next](../cluster02/)

This is the first of five nodes for cluster applications

address 172.17.1.92

user opsuser

## Services

  * HAProxy
  * [erddap](http://erddap.dm.marine.ie) running in docker (see below).

  * [ctd2cassandra](http://ctd2cassandra.dm.marine.ie)
    The process is managed by supervisor and should restart OK after server
    boot. There will be problems if kafka or cassandra are not running.

  * [fluorometer2cassandra](http://fluorometer2cassandra.dm.marine.ie)
    The process is managed by supervisor and should restart OK after server
    boot. There will be problems if kafka or cassandra are not running.

## Docker

To restart erddap after reboot:

    docker start erddap

To start a new erddap:

  docker run -d -p 8889:8080 -v /opt/erddap/content:/usr/local/tomcat/content rf/erddap

(You may want to remove the old erddap docker image and rename the newly running image).

