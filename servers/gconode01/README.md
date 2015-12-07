# gconode01

[previous](../gcoinstsrv02/) [next](../kafka01/)

This is the main data collection service at spiddal

address 172.16.255.226

user gcosuser

## Services

  * Kafka
Kafka runs in docker, and should restart automatically after a system reboot. The process
was launched with this command:

   docker run -t -d --name kafka \
   --restart always -p 2181:2181 \
   -p 9092:9092 \
   --env ADVERTISED_HOST=172.16.255.226 \
   --env ADVERTISED_PORT=9092 spotify/kafka
 
  * Data collectors (running by supervisor)

The data collectors are started automatically by superviser. These wait for two minutes of 
uptime when starting to give the kafka process time to be ready. Each exposes a mini http 
server to facilitate monitoring. Data is collected by reading from the tcp port provided
through the Moxa hardware switch (the Moxa exposes the serial data through tcp/ip).

    * bin/collect_adcp.sh
    * bin/collect_ctd.sh
    * bin/collect_fluorometer.sh
    * bin/collect_vemco.sh

  * Hydrophone rsync running by cron

Rsync was cross-compiled and copied to the hydrophone which exposes an ssh interface. The rsync
job is simply an rsync command running in cron to copy (and remove) the collected files from
the hydrophone each minute.

    flock -n /tmp/hydrophone.lock -c "rsync -avz --remove-source-files -e ssh --rsync-path bin/rsync icListen@172.16.255.253:Data /home/gcouser/hydrophone/"

