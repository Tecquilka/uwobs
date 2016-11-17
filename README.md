# uwobs
Underwater Observatory System

This public repository contains documentation, code and system configuration
for the data collection and processing system at <a href="spiddal.marine.ie">
spiddal.marine.ie</a>.

The target audience is uwobs system adminstrators. [Controlled Restart](ControlledRestart.md) procedures can be found [here](ControlledRestart.md)

[Adding a new collector](AddingANewCollector.md) procedures can be found [here](AddingANewCollector.md)

# Switching to/from Maintenance Mode

To turn the public website to maintenance mode use the rundeck job or the steps below:

    ssh dmuser@172.17.1.83 #dockerub
    cd ~/sites/spiddal.marine.ie/html
    ln -s -f index-maintenance.html index.html

To turn the public website to live mode use the rundeck job or the steps below:

    ssh dmuser@172.17.1.83 #dockerub
    cd ~/sites/spiddal.marine.ie/html
    ln -s -f index-live.html index.html


# Server Configurations

This uwobs documentation is maintained on each of the servers, with a script
provided to backup or restore configurations. (note proxy server is different
on spiddal hosts)

    cd ~/dev/uwobs
    https_proxy=10.0.5.55:80 git pull

To add/remove configuration files to be use add it to files.txt and use
[backup_config.sh](bin/backup_config.sh). <b>Be careful not to commit any
secrets to public git archive.</b> 

    vi servers/$(hostname)/files.txt

To backup some the configuration to git:

    cd ~/dev/uwobs
    https_proxy=10.0.5.55:80 git pull
    bin/backup_config.sh
    git commit -a -m 'latest configuration'
    https_proxy=10.0.5.55:80 git push

To restore some configuration file from git use [install_file.sh](bin/install_file.sh). For example, to recover haproxy configuration:

    sudo bin/install_file.sh /etc/haproxy/haproxy.cfg
    sudo service haproxy reload

# Shared Configurations
haproxy configuration is shared across cluster01-05. The following steps can be used to change the configuration on cluster01 and copy it to the other nodes.

    sudo vi /etc/haproxy/haproxy.cfg
    sudo service haproxy reload
    bin/backup_config.sh
    for server in 02 03 04 05; do cp servers/cluster01/files/etc/haproxy/haproxy.cfg servers/cluster${server}/files/etc/haproxy/haproxy.cfg; done
    git commit -a -m 'latest configuration'
    https_proxy=10.0.5.55:80 git push
    for item in 2 3 4 5 ; do ssh -t cluster0$item "cd dev/uwobs && https_proxy=10.0.5.55:80 git pull && sudo bin/install_file.sh /etc/haproxy/haproxy.cfg && sudo service haproxy reload" ; done



# General Overview
The system runs across two data centers, the shore station in Spiddal and the
main data center in Oranmore, having network connectivity between the zones.

Instruments are connected to the shore station in Spiddal where we have
4 uwobs primary servers:

## Servers in Spiddal
  * [spidvid](servers/spidvid/) a physical server with video card
  * [gconode01](servers/gconode01/) ubuntu vm running data collectors
  * [gcoinstsrv01](servers/gcoinstsrv01/) windows vm with vendor software
  * [gcoinstsrv02](servers/gcoinstsrv02/) windows vm with vendor software

## Servers in Oranmore:
  * [dockerub](servers/dockerub/) nginx server
  * [kafka01](servers/kafka01/) kafka server
  * [kafka02](servers/kafka02/) kafka server
  * [kafka03](servers/kafka03/) kafka server
  * [cluster01](servers/cluster01) haproxy, applications server
  * [cluster02](servers/cluster02) haproxy, applications server
  * [cluster03](servers/cluster03) haproxy, applications server
  * [cluster04](servers/cluster04) haproxy, applications server
  * [cluster05](servers/cluster05) haproxy, applications server

## Other servers also in Spiddal
There are a number of other servers in Spiddal, see spreadsheet from Damian for full list.
The following are referenced in these documents:
  * Asus2 Laptop 172.16.255.16
  * NMS Server 172.16.255.15
  * Hypervisor gco1 172.16.255.230

## Other servers also in Oranmore:
  * Hypervisor dmzdmvhost 172.17.1.84

## Other servers:
  * spidvid.cloudapp.net nginx video caching vm in azure.

