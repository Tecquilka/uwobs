#!/home/opsuser/venv/bin/python
import dateutil.parser
import datetime
import sys
import re

def _format(i):
  seconds = i % 60
  remainder = i - seconds
  minutes = remainder/60%60
  hours = (remainder/60 - minutes)/60
  return "{:02d}:{:02d}:{:02d}".format(hours,minutes,seconds)

def format_seconds(i):
   return "{0},000 --> {1},000".format(_format(i),_format(i+1))

filename_prog = re.compile('^(.*_(2\d{3}-\d\d-\d\d)_(\d\d)(\d\d)).mp4$')
def parse_date_filename(arg):
    match = filename_prog.match(arg)
    if match:
      s = '{0}T{1}:{2}:00Z'.format(match.group(2),match.group(3),match.group(4))
      start = dateutil.parser.parse(s)
      srt = '{0}.srt'.format(match.group(1))
      return (srt,start)
    return (None,None)

if len(sys.argv)>1:
  duration = 120
  for i in range(1,len(sys.argv)):
    arg = sys.argv[i]
    (srt,start) = parse_date_filename(arg)
    if srt:
      if len(sys.argv)>i+1:
        (x,next_start) = parse_date_filename(sys.argv[i+1])
        if next_start:
          duration = int((next_start-start).total_seconds())
      print srt,duration
# aja-helo-1H000314_2018-01-22_0414.mp4
      with open(srt,"w") as out:
         for i in range(0,duration):
            out.write(str(i+1)+'\n')
            t = start + datetime.timedelta(0,i)
            out.write(format_seconds(i)+'\n')
            out.write(t.isoformat()[:-6] + 'Z\n\n')

