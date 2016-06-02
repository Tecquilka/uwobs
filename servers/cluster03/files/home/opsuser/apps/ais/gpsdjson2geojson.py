#!/usr/bin/env python
import sys
from pykafka import KafkaClient
from pykafka.common import OffsetType
import datetime
import sys
from midas import WebServer, KillerMonitor, is_number
import argparse
import json
import pylru

cache = pylru.lrucache(10000)

parser = argparse.ArgumentParser(description='Consume stream of gpsd json and output stream of geojson.')
parser.add_argument('--timeout', type=int, default=600, help='Number of seconds to wait for messages before giving up, default=600 (10 minutes)')
parser.add_argument('--http-port', type=int, default=8077, help='HTTP web server port showing latest message, default is 8077')
parser.add_argument('--consume', type=str, required=True, help='the kafka topic containing gpsdjson to consume')
parser.add_argument('--publish', type=str, required=True, help='the kafka topic on which to publish geojson')
args = parser.parse_args()

client = KafkaClient(hosts="kafka01:9092,kafka02:9092,kafka03:9092")
subtopic = client.topics[args.consume]
consumer = subtopic.get_simple_consumer(auto_commit_enable=True,
                                     consumer_group="gpsdjson2geojson_v1", 
                                     auto_offset_reset=OffsetType.EARLIEST,
                                     reset_offset_on_start=False)

pubtopic = client.topics[args.publish]

sys.stderr.write("connected to kafka\n")

killer = KillerMonitor(args.timeout)
killer.setDaemon(True)
killer.start()
sys.stderr.write("Monitor will kill application if unable to process a message for %d seconds\n" % args.timeout)

webserver = WebServer(args.http_port)
webserver.setDaemon(True)
webserver.start()
sys.stderr.write("Web server running on port %d\n" % args.http_port)

with pubtopic.get_sync_producer() as producer:
  for message in consumer:
    if message is not None:
        o = None
        try:
          o = json.loads(message.value)
        except ValueError,e:
          continue
        if "mmsi" in o:
            mmsi = o["mmsi"]
            if not mmsi in cache:
               cache[mmsi] = {
                   "type": "Feature",
                   "geometry": {
                     "type": "Point",
                     "coordinates": [0, 0]
                   },
                   "properties": {
                     "mmsi": mmsi
                   }
                 }
            feature = cache[mmsi]
            feature["properties"].update(o)
            emitting = False
            if "lat" in o and "lon" in o:
                feature["properties"]["id"] = mmsi
                feature["geometry"]["coordinates"] = [float(o["lon"]),float(o["lat"])]
                emitting = True
            cache[mmsi] = feature
            if emitting:
                answer = json.dumps(feature)
                producer.produce(answer)
                webserver.update(feature)
                killer.ping()

