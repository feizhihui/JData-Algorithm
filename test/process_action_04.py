# encoding=utf-8
from datetime import datetime
import time
import pickle

date_begin = datetime(2016, 4, 1)
start_time = time.time()
# {user_id:[(sku_id,types,time)]}
actionMap = {}
# read F:/Datas/JData/JData_Action_201603_extra.csv
action_file = 'F:/Datas/JData/JData_Action_201604.csv'
infd = open(action_file, 'r')
infd.readline()
count = 0
for line in infd:
    tokens = line.strip().split(',')
    user_id = tokens[0]
    sku_id = tokens[1]
    action_type = tokens[4]
    detla_time = datetime.strptime(tokens[2], '%Y-%m-%d %H:%M:%S') - date_begin
    action_time = detla_time.days + detla_time.seconds / 86400
    assert action_time <= 15
    action_time = (1.3 ** action_time) / 50
    one_action = (sku_id, action_type, action_time)
    if user_id in actionMap:
        actionMap[user_id].append(one_action)
    else:
        actionMap[user_id] = [one_action]

    count += 1
    if count % 100000 == 0:
        print('readline ', count)

infd.close()
print('read over', action_file, len(action_file))

# sorted action by time
# {user_id:[(sku_id,types,time)]}
max_len = 0
min_len = 1 << 31
count = 0
for user_id, action_list in actionMap.items():
    sortedList = sorted(action_list, key=lambda x: (x[2], x[1], x[0]))
    actionMap[user_id] = sortedList
    if max_len < len(sortedList):
        max_len = len(sortedList)
    if min_len > len(sortedList):
        min_len = len(sortedList)
    count += 1
    if count % 1000 == 0:
        print('sort num', count)

print('step of action (%d, %d)' % (min_len, max_len))

print(time.time() - start_time)
print('begin to write pickle!')
output1 = open('DATA/actionMap04.pkl', 'wb')
pickle.dump(actionMap, output1)
