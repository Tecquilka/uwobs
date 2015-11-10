#!/usr/bin/env python
from datetime import datetime, timedelta,tzinfo

from astral import Astral

ZERO = timedelta(0)

class UTC(tzinfo):
  def utcoffset(self, dt):
    return ZERO
  def tzname(self, dt):
    return "UTC"
  def dst(self, dt):
    return ZERO

def is_it_daytime(lat,lon,delta_minutes):
   astral = Astral()
   sunrise = astral.sunrise_utc(datetime.today(),lat,lon)
   sunset = astral.sunset_utc(datetime.today(),lat,lon)
   return sunrise + timedelta(minutes=delta_minutes) < datetime.now(UTC()) < sunset - timedelta(minutes=delta_minutes)

def seconds_till_daytime(lat,lon,delta_minutes):
   if is_it_daytime(lat,lon,delta_minutes):
       return 0
   now = datetime.now(UTC())
   astral = Astral()
   sunrise = astral.sunrise_utc(now,lat,lon) + timedelta(minutes=delta_minutes)
   if sunrise < now:
      sunrise = astral.sunrise_utc(now + timedelta(hours=23),lat,lon) + timedelta(minutes=delta_minutes)
   return int((sunrise-now).total_seconds())+1

def seconds_till_daytime_ends(lat,lon,delta_minutes):
   if not is_it_daytime(lat,lon,delta_minutes):
       return 0
   now = datetime.now(UTC())
   astral = Astral()
   sunset = astral.sunset_utc(now,lat,lon) - timedelta(minutes=delta_minutes)
   answer = int((sunset-now).total_seconds())+1
   return answer

