# encoding=utf-8
from datetime import datetime
import time
import pickle

only_read = 1000000000000
date_begin = datetime(2016, 3, 17)
start_time = time.time()
# {user_id:[(sku_id,types,time)]}
actionMap = {}

action_file = 'F:/Datas/JData/JData_Action_201603.csv'
infd = open(action_file, 'r')
infd.readline()
ma_date = 0
for line in infd:
    tokens = line.strip().split(',')
    user_id = tokens[0]
    sku_id = tokens[1]
    action_type = tokens[4]
    action_time = datetime.strptime(tokens[2], '%Y-%m-%d %H:%M:%S') - date_begin
    action_time = action_time.days + action_time.seconds / 86400
    if action_time < 0:
        continue
    assert action_time <= 15
    action_time = (1.3 ** action_time) / 50
    if ma_date < action_time:
        ma_date = action_time
    one_action = (sku_id, action_type, action_time)
    if user_id in actionMap:
        actionMap[user_id].append(one_action)
    else:
        actionMap[user_id] = [one_action]
    only_read -= 1
    if only_read == 0:
        break
infd.close()
print('read over', action_file)
# sorted action by time
# {user_id:[(sku_id,types,time)]}
max_len = 0
min_len = 1 << 31
count = 0
for user_id, action_list in actionMap.items():
    # sortedList = sorted([(admId[2], admId[1], admId[0]) for admId in action_list])
    sortedList = sorted(action_list, key=lambda x: (x[2], x[1], x[0]))
    actionMap[user_id] = sortedList
    if max_len < len(sortedList):
        max_len = len(sortedList)
    if min_len > len(sortedList):
        min_len = len(sortedList)
    count += 1
    print('sorted %d in %d' % (count, len(actionMap.items())))

print('total user:', len(actionMap))
print('step of action (%d, %d)' % (min_len, max_len))

print(time.time() - start_time)
print('begin to write pickle!')
output1 = open('DATA/actionMap03.pkl', 'wb')
pickle.dump(actionMap, output1)
# output2 = open('DATA/user_id_map.pkl', 'wb')
# pickle.dump(list(user_id_map), output2)
# output3 = open('DATA/sku_id_map.pkl', 'wb')
# pickle.dump(list(sku_id_map), output3)

print('max date:', ma_date)
