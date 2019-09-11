#!/usr/bin/python3

from csv_select import select_one_from_csv

csv = 'https://raw.githubusercontent.com/IrishMarineInstitute/uwobs/master/common/apps/fluorometer_config.csv'
query = '''
SELECT * FROM csv
         WHERE reference='fluorometer0'
         AND start_date<date('now')
         AND end_date is null OR end_date > date('now')
         ORDER BY start_date DESC LIMIT 1
         '''
answer = select_one_from_csv(csv,query)
print('# {}'.format(answer))
# prints this:
# {'index': 3, 'reference': 'ctd0', 'type': 'ctd', 'manufacturer': 'idronaut', 'id': 'I-OCEAN7-304-1214551', 'moxa_server': '172.16.255.5', 'moxa_port': 950, 'start_date': '2019-05-03T10:00:00Z', 'end_date': None}
#
print ('''DEVICE={}
PORT={}
SERVER={}
FLUOROMETER_JSON_CONFIG='{"chl":{"scale_factor":{},"dark_counts":{}},"ntu":{"scale_factor":{},"dark_counts":{}}}'
'''.format(
    answer['id'],answer['moxa_port'],answer['moxa_server'],
    answer['chl_scale_factor'],answer['chl_dark_counts'],
    answer['ntu_scale_factor'],answer['ntu_dark_counts']
));

