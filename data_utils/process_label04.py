# encoding=utf-8

import pickle
from datetime import datetime

date_begin = datetime(2016, 4, 1)

label04_map = {}

action_file = 'F:/Datas/JData/JData_Action_201604.csv'
infd = open(action_file, 'r')
infd.readline()
for i, line in enumerate(infd):
    tokens = line.strip().split(',')
    user = tokens[0][:-2]
    sku_id = tokens[1]
    action_time = datetime.strptime(tokens[2], '%Y-%m-%d %H:%M:%S')
    if (action_time - date_begin).days > 5:
        continue

    action_type = tokens[4]
    if action_type == '4':
        label04_map[user] = sku_id
    if i % 1000000 == 0:
        print('iters', i + 1)
print('test dataset lens:', len(label04_map))
print('begin to dump!')
infd.close()
output = open('DATA/label04_map.pkl', 'wb')
pickle.dump(label04_map, output)
