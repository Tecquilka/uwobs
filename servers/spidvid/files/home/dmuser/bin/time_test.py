#!/usr/bin/env python
from daytimes import *
from local_info import lat, lon, delta_minutes
daytime = is_it_daytime(lat,lon,delta_minutes)
if(daytime):
  print "seconds till daytime ends: ", seconds_till_daytime_ends(lat,lon,delta_minutes)
else:
  print "seconds till daytime: ", seconds_till_daytime(lat,lon,delta_minutes)

