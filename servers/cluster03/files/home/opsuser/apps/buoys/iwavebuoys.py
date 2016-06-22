import requests
import json

proxies = { "http": "http://10.0.5.55:80" }
url = "http://erddap.marine.ie/erddap/tabledap/IWaveBNetwork30Min.json?longitude,latitude,time,station_id,PeakPeriod,PeakDirection,UpcrossPeriod,SignificantWaveHeight,SeaTemperature,Hmax,THmax,MeanCurDirTo,MeanCurSpeed,SignificantWaveHeight_qc,PeakPeriod_qc&time%3E=now-8hours"
r = requests.get(url,proxies=proxies)
d = r.json()
data = {}
station_id = -1
colnames = d["table"]["columnNames"];
for i,val in enumerate(colnames):
   if val == "station_id":
      station_id = i
      break

for row in d["table"]["rows"]:
   station = row[station_id]
   if not station in data:
      data[station] = {}
   o = data[station]
   for i,val in enumerate(row):
      if val is not None and not colnames[i] in o:
          o[colnames[i]] = val

for key in data:
    print json.dumps(data[key])
