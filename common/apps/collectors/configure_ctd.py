#!/usr/bin/python3

from csv_select import select_one_from_csv

csv = 'https://raw.githubusercontent.com/IrishMarineInstitute/uwobs/master/common/apps/test.csv'
query = '''
SELECT * FROM csv
         WHERE reference='ctd0'
         AND start_date<date('now')
         AND end_date is null OR end_date > date('now')
         ORDER BY start_date DESC LIMIT 1
         '''
answer = select_one_from_csv(csv,query)
print('# {}'.format(answer))
# prints this:
# {'index': 3, 'reference': 'ctd0', 'type': 'ctd', 'manufacturer': 'idronaut', 'id': 'I-OCEAN7-304-1214551', 'server': '172.16.255.5', 'port': 950, 'start_date': '2019-05-03T10:00:00Z', 'end_date': None}
#
print ('''DEVICE={}
PORT={}
SERVER={}'''.format(answer['id'],answer['port'],answer['server']));

