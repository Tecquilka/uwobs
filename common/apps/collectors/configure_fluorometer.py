#!/usr/bin/python3
import json

from csv_select import select_one_from_csv

csv = 'https://raw.githubusercontent.com/IrishMarineInstitute/uwobs/master/common/apps/fluorometer_config.csv'
query = '''
SELECT * FROM csv
         WHERE reference='fluorometer0'
         AND start_date<=datetime('now')
         AND end_date is null OR end_date >= datetime('now')
         ORDER BY start_date DESC LIMIT 1
         '''
#query = "select * from csv"
answer = select_one_from_csv(csv,query)
print('# {}'.format(answer))
# prints this:
# {'end_date': None, 'type': 'fluorometer', 'moxa_port': 951, 'chl_dark_counts': 48, 'ntu_scale_factor': 0.0529, 'chl_scale_factor': 0.0178, 'reference': 'fluorometer0', 'moxa_server': '172.16.255.5', 'ntu_dark_counts': 41, 'id': 'WL_ECO_FLNTU-4476', 'manufacturer': 'seabird', 'start_date': '2019-09-11T00:00:00Z'}
#
FLUOROMETER_CONFIG = '{}|{}|{}|{}'.format( 
               answer['chl_scale_factor'],
              answer['chl_dark_counts'],
              answer['ntu_scale_factor'],
              answer['ntu_dark_counts']
         )
print ('''DEVICE={}
PORT={}
SERVER={}
FLUOROMETER_CONFIG='{}'
'''.format(
    answer['id'],answer['moxa_port'],answer['moxa_server'],FLUOROMETER_CONFIG
));

