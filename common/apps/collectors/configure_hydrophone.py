#!/usr/bin/python3

from csv_select import select_one_from_csv

csv = 'https://raw.githubusercontent.com/IrishMarineInstitute/uwobs/master/common/apps/hydrophone_config.csv'
query = '''
SELECT * FROM csv
         WHERE reference='hydrophone0'
         AND start_date<=datetime('now')
         AND end_date is null OR end_date >= datetime('now')
         ORDER BY start_date DESC LIMIT 1
         '''
answer = select_one_from_csv(csv,query)
print('# {}'.format(answer))
# prints this:
# {'index': 1, 'reference': 'hydrophone0', 'type': 'hydrophone', 'manufacturer': 'OceanSonics', 'id': 'SBF1622', 'ip_address': '172.16.255.254', 'start_date': '2019-09-13T10:00:00Z', 'end_date': None}
#
print ('''DEVICE={}
SERVER={}'''.format(answer['id'],answer['server']));

