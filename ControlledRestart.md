# Controlled Restart
This section captures the steps to shutdown and restart the
complete system of instruments and virtual machines. Note that if physical
servers (the NMS, hypervisors, spidvid) are stopped then manual intervention
may be required to restart those. That scenario is not considered here.

## Controlled Shutdown

### 0. Turn site on maintenance mode
Use the [rundeck job](http://rundeck.dm.marine.ie/project/uwobs/jobs/spiddal.marine.ie)

### 1. Turn off the underwater devices
Remote desktop to the NMS Server 172.16.255.15 and logon to the Espy Client as user System Administrator. Navigate the menu:
  * Object Administrator
    * Managed Elements Catalog
      * Galway PNC Node T...
        * CEE1-NODE-1`
          * (Configuration Tab)

Power off all the science ports:
  * 1 (Hydrophone)
  * 6 (CTD)
  * 7 (Turb/Fluor)
  * 10 (Vemco)
  * 12 (ADCP)
  * 18 (HDTV)

### 2. Turn off Spiddal virtual machines
Shut down the windows and linux vms by connecting to them and issuing the appropriate commands.
  * [gcoinstsrv01 172.16.255.225](servers/gcoinstsrv01/) windowsvm
  * [gcoinstsrv02 172.16.255.227](servers/gcooinstsrv02/) windowsvm
  * [gconode01 172.16.255.226](servers/gconode01/) Use rundeck

### 3. Turn off Oranmore virtual machines
Use one of the following two methods
#### A. Use [rundeck job](http://rundeck.dm.marine.ie/project/uwobs/jobs/cluster) to perform the following actions:
  * 1 Stop kafka vms
  * 2 Stop data vms
  * 3 Stop cluster01-04 vms
  * 4 Stop rundeck vm NB this may not work in which case use ssh to [cluster05 172.17.1.96](servers/cluster05)

#### B. From the Command Line
From a shell on [cluster01](servers/cluster01) you can easily shutdown the servers with the following
command which will prompt for passwords if required.

    for server in kafka01 kafka02 kafka03 data01 data02 data03 cluster05 cluster04 cluster03 cluster02
    do echo $server && ssh -t $server 'sudo shutdown -h now'
    done
    sudo shutdown -h now

### 4. Turn off the web server [dockerub](servers/dockerub/)
<b>NB:</b> Note this vm is in a main dmz hypervisor controlled by operations. When power cycling [dockerub](servers/dockerub/) use `shutdown -r now` unless Keith or Colin are available to restart that vm from the hypervisor.

## Controlled Startup
### 1. Start the dockerub server first so the web interface becomes available.
  * [dockerub](servers/dockerub/)

### 2. Turn on the underwater devices
Remote desktop to the NMS Server 172.16.255.15 and logon to the Espy Client as user System Administrator. Navigate the menu:
  * Object Administrator
    * Managed Elements Catalog
      * Galway PNC Node T...
        * CEE1-NODE-1`
          * (Configuration Tab)

Power on the following science ports:
  * 1 (Hydrophone)
  * 6 (CTD)
  * 7 (Turb/Fluor)
  * 10 (Vemco)
  * 12 (ADCP)
  * 18 (HDTV)

### 3. Turn on Spiddal virtual machines
The Spiddal VM's can be started from hypervisor gco1 172.16.255.230
Use powershell script [C:\Users\Administrator\Desktop\start_uwobs_vms.ps1](servers/gco1/files/Users/Administrator/Desktop/start_uwobs_vms.ps1)
  * [gcoinstsrv01](servers/gcoinstsrv01/)
  * [gcoinstsrv02](servers/gcooinstsrv02/)
  * [gconode01](servers/gconode01/)

### 4. Adjust time on Devices
Remote desktop to [gcoinstsrv01](servers/gcoinstsrv01/)
  * Start the Idronaut Terminal software and connect to com 7 at 9600 baud. Stop the feed using `ctrl-c`,
then use the menu options to set the date and time. Verify, then restart streaming.
  * Use Chrome to connect to the [hydrophone](http://172.16.255.253/operations.html) using the bookmarked link. The device may
have continued running on battery and have the correct time, otherwise use the web interface to reset the time.

### 5. Turn on Oranmore virtual machines
Now the Spiddal VM's can be started from hypervisor dmzdmvhost 172.17.1.84

Use powershell script [C:\Users\Administrator\Desktop\start_uwobs_vms.ps1](servers/dmzdmvhost/files/Users/Administrator/Desktop/start_uwobs_vms.ps1)

The following VM' will be started:
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

### 6. Adjust the video
Remote desktop to the NMS Server 172.16.255.15
  * Start the Kongsberg software using the “Kconbsberg Camera Control” shortcut on Desktop
  * Start VLC media player using “VLC Spiddal Video” shortcut on Desktop. (Note it takes a couple of seconds to show the video)
  * The Kongsberg software can now be used to control the video, which will show adjust with about a 2 second delay.  At the moment we are using an upward looking position currently stored at “Preset 7” (Preset 3 during biofoul episode Nov 2015).
  * If the picture remains black or very dark (possibly due to biofouling), it may be necessary to change the exposure from automatic to shutter, and slow the shutter speed until picture becomes visible.
  * If all else fails set auto focus and try various presets or resort to manually searching for something visible.

### 7. Restart some added services
  * Run the (start all docker services)[http://rundeck.dm.marine.ie/project/uwobs/jobs/docker] rundeck job.

### 8. check the dashboard
  * (uwobs dashboard)[http://dashboard.sysadmin.dm.marine.ie/]

### 9. Turn site off maintenance mode
Use the [rundeck job](http://rundeck.dm.marine.ie/project/uwobs/jobs/spiddal.marine.ie)
