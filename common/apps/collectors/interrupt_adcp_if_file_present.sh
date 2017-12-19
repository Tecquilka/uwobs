#!/bin/sh

 if [ ! -f /tmp/adcp-paused ]; then
    exit 0;
 fi

SERVER=172.16.255.8
PORT=952
COMMAND_PORT=968
#!/bin/sh

echo killing any adcp processes >&2

kill $(ps -ef | grep adcp | grep -v grep  | grep -v interrupt | awk '{print $2}') || echo no process killed >&2

python -c "
from serial import rfc2217,serial_for_url,Serial
from time import sleep
import datetime
import sys,socket, threading
s = serial_for_url('socket://$SERVER:$PORT',baudrate=9600,timeout=1)
def ComPortThread():
      while alive.isSet():
            b = s.read(s.inWaiting() or 1)
            if b:
                b = b.replace(b'\r\n', b'\n')
                try:
                   sys.stdout.write(b.decode())
                except:
                   print '(decode)'
                   pass
            else:
                sleep(0.5)

thread = threading.Thread(target=ComPortThread)
thread.setDaemon(1)
alive = threading.Event()
alive.set()
thread.start()

control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
control.connect(('$SERVER',$COMMAND_PORT))
control.send('\x21\x00')
sleep(0.4)
control.send('\x22\x00')
sys.stdout.write('sent break... waiting 5 seconds to continue\n')
sleep(5)
control.send('\x21\x00')
sleep(0.4)
control.send('\x22\x00')
sys.stdout.write('resent break... waiting another 5 seconds to continue\n')
sleep(5)
alive.clear()
thread.join()
s.close()
control.close()
"

echo done >&2
