#!/usr/bin/env python
import sys
from pykafka import KafkaClient
from pykafka.common import OffsetType
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
import datetime
import sys
from midas import WebServer, KillerMonitor, is_number
import argparse

parser = argparse.ArgumentParser(description='Stream ctd data from kafka to cassandra.')
parser.add_argument('--timeout', type=int, default=300, help='Number of seconds to wait for messages before giving up, default=300 (5 minutes)')
parser.add_argument('--http-port', type=int, default=8082, help='HTTP web server port showing latest message, default is 8082')
parser.add_argument('--verbose', type=bool, default=False, help='Whether to write to the console')
args = parser.parse_args()

lat = 53.227333
lon = -9.266286
depth = 20.0
cluster = Cluster(['data01','data02','data03'])
session = cluster.connect('das')
prepared_insert = SimpleStatement("""
    INSERT INTO ctd (instrument_id, time, lat, lon, depth, press, temp, cond, sal, soundv, ttime)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                   """)
sys.stderr.write("connected to cassandra\n")
client = KafkaClient(hosts="kafka01:9092,kafka02:9092,kafka03:9092")
topic = client.topics['spiddal-ctd']
consumer = topic.get_simple_consumer(auto_commit_enable=True,
                                     consumer_group="ctd2cassandra_v2", 
                                     auto_offset_reset=OffsetType.EARLIEST,
                                     reset_offset_on_start=False)

sys.stderr.write("connected to kafka\n")

killer = KillerMonitor(args.timeout)
killer.setDaemon(True)
killer.start()
sys.stderr.write("Monitor will kill application if unable to process a message for %d seconds\n" % args.timeout)

webserver = WebServer(args.http_port)
webserver.setDaemon(True)
webserver.start()
sys.stderr.write("Web server running on port %d\n" % args.http_port)

if args.verbose:
    sys.stdout.write("\n")
for message in consumer:
   if message is not None:
        (timestamp,source,data) = message.value.split('|',3)
        values = data.split()
        if(len(values) == 6) and all(is_number(i) for i in values[0:5]):

            (Press,Temp,Cond,Sal,SoundV,Time) = values
            session.execute(
                prepared_insert,(source,timestamp,lat,lon,depth,float(Press),float(Temp),float(Cond),float(Sal),float(SoundV),Time)
            )
            killer.ping()
            webserver.update(message.value)
            if args.verbose:
                sys.stdout.write("\r{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}".format(source,timestamp,Press,Temp,Cond,Sal,SoundV,Time))
                sys.stdout.flush()
