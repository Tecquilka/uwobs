#Adding a New Collector

This document describes the steps involved to add a new collector.

##0. Before you start
Be sure to have the latest uwobs.

    cd ~/dev/uwobs
    https_proxy=10.0.5.55:80 git pull

##1. Identify your device
The device to be collected should expose line oriented data via a tcp port. For an AIRMAR or other nmea serial device, consider using [kplex](http://www.stripydog.com/kplex/overview.html) to expose data via tcp.

You'll need to know the following information about the device:
  * type: eg ais, airmar, adcp etc.
  * location: eg rinville, spiddal etc.
  * id: a short unique identifier, eg 1 or KN247
  * server: the server on which the device can be reached via tcp
  * port: the tcp port for the device
  * http_port: an unused http port typically in the 8000-8999 range

##2. Verify network access
From the collector host, verify you can connect to the server and port of the device using telnet.

##3. Create a collector script.
Begin with a copy of a similar [collector](https://github.com/IrishMarineInstitute/uwobs/tree/master/common/apps/collectors) following the naming convention.
And fill in the blanks using the information which you already identified about your device.

##4. Add a supervisor configuration
Begin with a copy of a [similar supervisor configuration](https://github.com/IrishMarineInstitute/uwobs/blob/master/servers/cluster02/files/etc/supervisor/conf.d/airmar-rinville-1.conf)

##5. Start the new collector
Use supervisorctl to read and add the configuration.

    sudo supervisorctl reread
    sudo supervisorctl add my-new-collector
    sudo supervisorctl start my-new-collecto

##6. Add to haproxy
Typically about 4 lines in /etc/haproxy/haproxy.cfg. Look for the airmar-rinville-1 example.

    sudo service haproxy reload

##7. Backup the configuration and push to git

    bin/backup_config.sh
    bin/backup_haproxy.sh
    git status
    git add #whatever new files to be added

##8. Update haproxy on all servers

Use rundeck and run the cluster/git_pull_uwobs job, followed by cluster/reload_haproxy job.

##9. Add to the monitoring dashboard

Add your collector at on the [dashboard](http://dashboard.sysadmin.dm.marine.ie/). When happy, use Save Freeboard (pretty), and replace the [monitoring-dashboard json file](https://github.com/IrishMarineInstitute/uwobs/blob/master/common/monitoring-dashboard/dashboard.json) (currently on cluster02).

Don't forget to push your changes back to git!
