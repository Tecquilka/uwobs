#!/usr/bin/python3
from serial import rfc2217,serial_for_url,Serial
from time import sleep
import datetime
import sys,socket, threading
import requests
import traceback

from csv_select import select_one_from_csv
csv = 'https://raw.githubusercontent.com/IrishMarineInstitute/uwobs/master/common/apps/adcp_config.csv'
txt = 'https://raw.githubusercontent.com/IrishMarineInstitute/uwobs/master/common/apps/adcp_config.txt'

def get_adcp_commands(url):
  response = requests.get(url,
     headers={'Cache-Control': 'no-cache'})
  lines = [line.strip(' \t\r\n') for line in response.text.splitlines()]
  # filter out blanks and comments
  return [line for line in lines if line != '' and not line.startswith('#')]


def reconfigure_adcp(server,port,command_port,commands):
  s = serial_for_url('socket://{0}:{1}'.format(server,port),baudrate=9600,timeout=1)

  def ComPortThread():
        while alive.isSet():
              b = s.read(s.inWaiting() or 1)
              if b:
                  b = b.replace(b'\r\n', b'\n')
                  try:
                     sys.stderr.write('>>> {1}\n'.format(b.decode()))
                  except:
                     print('(decode)')
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
  brk1 = b'\x21\x00'
  brk2 = b'\x22\x00'
  control.send(brk1)
  sleep(0.4)
  control.send(brk2)
  sys.stderr.write('sent break... waiting 5 seconds to continue\n')
  sleep(5)
  control.send(brk1)
  sleep(0.4)
  control.send(brk2)
  sys.stderr.write('resent break... waiting another 5 seconds to continue\n')
  sleep(5)
  control.send(brk1)
  sleep(0.4)
  control.send(brk2)
  sys.stderr.write('resent break... waiting another 5 seconds to continue\n')
  sleep(5)
  control.send(brk1)
  sleep(0.4)
  control.send(brk2)
  sys.stderr.write('resent break... waiting another 5 seconds to continue\n')
  sleep(5)
  control.send(brk1)
  sleep(0.4)
  control.send(brk2)
  sys.stderr.write('resent break... waiting another 5 seconds to continue\n')
  sleep(5)

  s.write('CR1\r'.encode())
  sleep(0.5)
  tt='TT{0}\r'.format(datetime.datetime.utcnow().strftime('%Y/%m/%d, %H:%M:%S'))
  s.write(tt.encode())
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

query = '''
SELECT * FROM csv
         WHERE reference='adcp0'
         AND start_date<=datetime('now')
         AND end_date is null OR end_date >= datetime('now')
         ORDER BY start_date DESC LIMIT 1
         '''
answer = select_one_from_csv(csv,query)
print('# {}'.format(answer))
# prints this:
# # {'end_date': None, 'type': 'adcp', 'moxa_server': '172.16.255.5', 'moxa_command_port': 968, 'reference': 'adcp0', 'start_date': '2019-09-11', 'manufacturer': 'teledyne', 'id': 'TRDI-WHB600Hz-10488', 'moxa_port': 952, 'configure_on_startup': 1}
#
if answer['configure_on_startup']:
  sys.stderr.write('will try to send reconfigure commands to the device\n')
  try:
    commands = get_adcp_commands(txt)
    reconfigure_adcp(answer['moxa_server'],answer['moxa_port'],answer['moxa_command_port'],commands)
  except Exception as e:
    print("reconfigure error" + str(e), file=sys.stderr)
    print(traceback.format_exc(), file=sys.stderr)

print ('''DEVICE={}
PORT={}
SERVER={}'''.format(answer['id'],answer['moxa_port'],answer['moxa_server']));

