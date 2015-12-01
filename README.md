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
4 uwobs primary servers:

## Servers in Spiddal
  * [spidvid](servers/spidvid/) a physical server with video card
  * [gconode01](servers/gconode01/) ubuntu vm running data collectors
  * [gcoinstsrv01](servers/gcoinstsrv01/) windows vm with vendor software
  * [gcoinstsrv02](servers/gcooinstsrv02/) windows vm with vendor software



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
  * Asus2 Laptop
  * NMS Server
  * Hypervisor gco1
  * Hypervisor gco2

## Other servers also in Oranmore:
  * Hypervisor 172.17.1.84

## Other servers:
  * spidvid.cloudapp.net nginx video caching vm in azure.

# Controlled Restart
This section attempts to capture the steps to shutdown and restart the
complete system of instruments and virtual machines. Note that if physical
servers (the NMS, hypervisors, spidvid) are stopped then manual intervention
may be required to restart those. That scenario is not considered here.
## Controlled Shutdown

After using the pnc client to stop all the devices, do a soft shutdown of vms in the following order:
  * [gcoinstsrv01](servers/gcoinstsrv01/)
  * [gcoinstsrv02](servers/gcooinstsrv02/)
  * [gconode01](servers/gconode01/)
  * [kafka01](servers/kafka01/)
  * [kafka02](servers/kafka02/)
  * [kafka03](servers/kafka03/)
  * [data01](servers/data01/)
  * [data02](servers/data02/)
  * [data03](servers/data03/)
  * [cluster05](servers/cluster05)
  * [cluster04](servers/cluster04)
  * [cluster03](servers/cluster03)
  * [cluster02](servers/cluster02)
  * [cluster01](servers/cluster01)
  * [dockerub](servers/dockerub/)


## Controlled Startup
Start the vm's in the following order, then use the pnc client to restart the devices
  * [dockerub](servers/dockerub/)
  * [gcoinstsrv01](servers/gcoinstsrv01/)
  * [gcoinstsrv02](servers/gcooinstsrv02/)
  * [gconode01](servers/gconode01/)
  (devices could be restarted at any point from now)
  * [cluster01](servers/cluster01)
  * [cluster02](servers/cluster02)
  * [cluster03](servers/cluster03)
  * [cluster04](servers/cluster04)
  * [cluster05](servers/cluster05)
  * [kafka01](servers/kafka01/)
  * [kafka02](servers/kafka02/)
  * [kafka03](servers/kafka03/)
  * [data01](servers/data01/)
  * [data02](servers/data02/)
  * [data03](servers/data03/)

