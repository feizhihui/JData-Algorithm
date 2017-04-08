# encoding=utf-8
import time

start_time = time.time()
action_file = 'F:/Datas/JData/JData_Action_201604.csv'
# {user_id:[(sku_id,types,time)]}
target_actionMap = {}

infd = open(action_file, 'r')
infd.readline()
for line in infd:
    tokens = line.strip().split(',')
    user_id = tokens[0]
    sku_id = tokens[1]
    action_type = tokens[4]
    if action_type != '4':
        continue
    if user_id not in target_actionMap:
        target_actionMap[user_id] = [sku_id]
    else:
        target_actionMap[user_id].append(sku_id)
infd.close()

print('ordered total user:', len(target_actionMap))
print(target_actionMap['12025'])
print(time.time() - start_time)
