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
import json

parser = argparse.ArgumentParser(description='Stream dcu ysi mestech data from kafka to cassandra.')
parser.add_argument('--timeout', type=int, default=3600, help='Number of seconds to wait for messages before giving up, default=3600 (1 hour)')
parser.add_argument('--http-port', type=int, default=8084, help='HTTP web server port showing latest message, default is 8084')
parser.add_argument('--verbose', type=bool, default=False, help='Whether to write to the console')
parser.add_argument('--instrument_id', required=True, help='the instrument_id')
parser.add_argument('--site_id', required=True, help='the site_id')
parser.add_argument('--lat', type=float, required=True, help='the instrument latitude')
parser.add_argument('--lon', type=float, required=True, help='the instrument longitude')
args = parser.parse_args()

lat = args.lat
lon = args.lon
site_id = args.site_id
instrument_id = args.instrument_id

cluster = Cluster(['data01','data02','data03'])
session = cluster.connect('das')
prepared_insert = SimpleStatement("""
    INSERT INTO mestech (instrument_id, time, site_id, lat, lon, clock_date, clock_time, temp, cond, salinity, depth, ph, ph_mv, turbidity, do_mgl, battery)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                   """)
sys.stderr.write("connected to cassandra\n")
client = KafkaClient(hosts="kafka01:9092,kafka02:9092,kafka03:9092")
topic = client.topics[instrument_id]
consumer = topic.get_simple_consumer(auto_commit_enable=True,
                                     consumer_group="ysi2cassandra_v1", 
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
        values = message.value.split(',')
        if(len(values) >= 11) and all(is_number(i) for i in values[2:10]):

            (clock_date, clock_time, temp, cond, salinity, depth, ph, ph_mv, turbidity, do_mgl, battery,dummy) = values
            (dd,mm,yyyy) = clock_date.split('/')
            timestamp = "{0}-{1}-{2}T{3}Z".format(yyyy,mm,dd,clock_time)
            session.execute(
                prepared_insert,(instrument_id,timestamp,site_id,lat,lon,clock_date,clock_time,float(temp),float(cond),float(salinity),
                                 float(depth), float(ph), float(ph_mv), float(turbidity), float(do_mgl), float(battery))
            )
            killer.ping()
            webserver.update(message.value)
            if args.verbose:
                print json.dumps({"clock_date": clock_date, "clock_time": clock_time, "temp": temp, "cond": cond,
                      "salinity": salinity, "depth": depth, "ph":ph, "ph_mv": ph_mv, "turbidity": turbidity, "do_mgl": do_mgl, "battery": battery})
