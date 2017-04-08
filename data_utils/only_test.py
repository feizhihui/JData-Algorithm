# encoding=utf-8
from datetime import datetime
import time
import pandas as pd

start_time = time.time()
action_file = 'F:/Datas/JData/JData_Action_201603_extra.csv'
# {user_id:[(sku_id,types,time)]}
actionMap = {}
infd = open(action_file, 'r')

pan = pd.read_csv(action_file, usecols=['user_id', 'sku_id', 'time', 'type'])
print(time.time() - start_time)
actionMap = {}
for name, group in pan.groupby('user_id'):
    print(name)
    actionMap[name] = []
    for line in group.iterrows():
        print(line)
        actionMap[name].append((line['sku_id'], line['type'], line['time']))

# actionMap[name]=

print(len(actionMap))
