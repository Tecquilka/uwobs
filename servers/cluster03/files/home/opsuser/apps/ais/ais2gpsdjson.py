#!/usr/bin/env python
import sys
import argparse
import subprocess
import os
from midas import WebServer, KillerMonitor

parser = argparse.ArgumentParser(description='Reads ais data from kafka, converts to json using gpsd, and writes to kafka')
parser.add_argument('--timeout', type=int, default=600, help='Number of seconds to wait for messages before giving up, default=600 (10 minutes)')
parser.add_argument('--http-port', type=int, default=8078, help='HTTP web server port showing latest message, default is 8078')
args = parser.parse_args()

killer = KillerMonitor(args.timeout)
killer.setDaemon(True)
killer.start()
sys.stderr.write("Monitor will kill application if unable to process a message for %d seconds\n" % args.timeout)

webserver = WebServer(args.http_port)
webserver.setDaemon(True)
webserver.start()
sys.stderr.write("Web server running on port %d\n" % args.http_port)

offsets_dir = "/var/lib/consumer-offsets/ais-rinville-1-2gpsdjson"
if not os.path.exists(offsets_dir):
    os.makedirs(offsets_dir)


command = """kafkacat -X topic.offset.store.path=/var/lib/consumer-offsets/ais-rinville-1-2gpsdjson -o stored -C -u -b kafka01,kafka02,kafka03 -t ais-rinville-1 | stdbuf -oL sed -e 's/^[^|]*|[^|]*|//' | stdbuf -oL gpsdecode | stdbuf -oL kafkacat -P -T -b kafka01,kafka02,kafka03 -p 0 -t ais-rinville-1-gpsdjson """
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
for line in iter(process.stdout.readline, ''):
        killer.ping()
        webserver.update(line)
