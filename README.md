# uwobs
Underwater Observatory System

This public repository contains documentation, code and system configuration
for the data collection and processing system at <a href="spiddal.marine.ie">
spiddal.marine.ie</a>.

The target audience is uwobs system adminstrators.

Additional documentation will be added in coming weeks, for now the important
configurations and applications can be found under the servers folder.

# General Overview
The system runs across two data centers, the shore station in Spiddal and the
main data center in Oranmore, having network connectivity between the zones.

Instruments are connected to the shore station in Spiddal where we have
2 uwobs primary servers:

## Servers in Spiddal
  * [spidvid](servers/spidvid/) a physical server with video card
  * [gconode01](servers/gconode01/] ubuntu vm running data collectors

## Servers in Oranmore:
  * [dockerub](servers/dockerub/) nginx server
  * [kafka01](servers/kafka01/) kafka server
  * [kafka02](servers/kafka02/) kafka server
  * [kafka03](servers/kafka03/) kafka server
  * [data01](servers/data01/) cassandra, elasticsearch server
  * [data02](servers/data02/) cassandra, elasticsearch server
  * [data03](servers/data03/) cassandra, elasticsearch server
  * [cluster01](servers/cluster01) haproxy, applications server
  * [cluster02](servers/cluster02) haproxy, applications server
  * [cluster03](servers/cluster03) haproxy, applications server
  * [cluster04](servers/cluster04) haproxy, applications server
  * [cluster05](servers/cluster05) haproxy, applications server

## Other servers also in Spiddal:
  * gconode02 is a windows having with vendor applications for configuring
  * Asus2 Laptop
  * NMS Server
  * Hypervisor.

## Other servers also in Spiddal:
  * Hypervisor 172.17.1.84

## Other servers:
  * spidvid.cloudapp.net nginx video caching vm in azure.
