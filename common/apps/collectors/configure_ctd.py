#!/usr/bin/python3
from serial import rfc2217,serial_for_url,Serial
from time import sleep
import datetime
import sys,socket, threading
import requests
import traceback

from csv_select import select_one_from_csv
csv = 'https://raw.githubusercontent.com/IrishMarineInstitute/uwobs/master/common/apps/ctd_config.csv'
txt = 'https://raw.githubusercontent.com/IrishMarineInstitute/uwobs/master/common/apps/ctd_config.txt'

def get_ctd_commands(url):
  response = requests.get(url,
     headers={'Cache-Control': 'no-cache'})
  lines = [line.strip(' \t\r\n') for line in response.text.splitlines()]
  timestamp = datetime.datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S')
  # filter out blanks and comments
  return [line for line in lines if line != '' and not line.startswith('#')]


def reconfigure_ctd(server,port,command_port,commands):
  s = serial_for_url('socket://{0}:{1}'.format(server,port),baudrate=9600,timeout=1)

  def ComPortThread():
        while alive.isSet():
              b = s.read(s.inWaiting() or 1)
              if b:
                  b = b.replace(b'\r\n', b'\n')
                  try:
                     sys.stderr.write('>>> {1}\n'.format(b.decode()))
                  except:
                     print('(decode)', file=sys.stderr)
                     pass
              else:
                  sleep(0.5)

  thread = threading.Thread(target=ComPortThread)
  thread.setDaemon(1)
  alive = threading.Event()
  alive.set()
  thread.start()

  control = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  control.connect((server,command_port))
  brk = b'\x03'
  control.send(brk)
  sleep(0.4)
  control.send(brk)
  sys.stderr.write('sent break... waiting 5 seconds to continue\n')
  sleep(5)

  #s.write(tt.encode())
  sleep(0.5)
  for line in commands:
      chars = '{0}\r'.format(line)
      sent = s.write(chars.encode())
      sys.stderr.write('{0}\t{1}\n'.format(sent,line))
      sleep(1)
  alive.clear()
  thread.join()
  s.close()
  control.close()

#!/usr/bin/python3

query = '''
SELECT * FROM csv
         WHERE reference='ctd0'
         AND start_date<=datetime('now')
         AND end_date is null OR end_date >= datetime('now')
         ORDER BY start_date DESC LIMIT 1
         '''
answer = select_one_from_csv(csv,query)
print('# {}'.format(answer))
# prints this:
# {'index': 3, 'reference': 'ctd0', 'type': 'ctd', 'manufacturer': 'idronaut', 'id': 'I-OCEAN7-304-1214551', 'moxa_server': '172.16.255.5', 'moxa_port': 950, 'start_date': '2019-05-03T10:00:00Z', 'end_date': None}
#
if answer['configure_on_startup']:
  sys.stderr.write('will try to send reconfigure commands to the device\n')
  try:
    commands = get_ctd_commands(txt)
    reconfigure_ctd(answer['moxa_server'],answer['moxa_port'],answer['moxa_command_port'],commands)
  except Exception as e:
    print("reconfigure error" + str(e), file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)

print ('''DEVICE={}
PORT={}
SERVER={}'''.format(answer['id'],answer['moxa_port'],answer['moxa_server']));

