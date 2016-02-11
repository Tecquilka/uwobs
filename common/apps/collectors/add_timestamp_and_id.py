#!/usr/bin/env python
import datetime
import sys
if len(sys.argv) != 2:
   sys.stderr.write("Usage: {0} IDENTIFIER\n".format(sys.argv[0]))
   sys.exit(2)
id=sys.argv[1]
try:
  while True:
    line = sys.stdin.readline()
    if not line:
        break
    now = datetime.datetime.utcnow().isoformat()[:-3]+"Z"
    print("{0}|{1}|{2}".format(now,id,line.rstrip("\n")))
except (KeyboardInterrupt, SystemExit):
    pass
