# encoding=utf-8

import pickle

sku_id_map = {}

action_file = 'F:/Datas/JData/JData_Product.csv'
infd = open(action_file, 'r')
infd.readline()
for i, line in enumerate(infd):
    tokens = line.strip().split(',')
    sku_id = tokens[0]
    sku_id_map[sku_id] = i

infd.close()
output = open('DATA/sku_id_map.pkl', 'wb')
pickle.dump(sku_id_map, output)

user_id_map = {}
action_file = 'F:/Datas/JData/JData_User.csv'
infd = open(action_file, 'r')
infd.readline()
for i, line in enumerate(infd):
    tokens = line.strip().split(',')
    user_id = tokens[0]
    user_id_map[user_id] = i

infd.close()
output = open('DATA/user_id_map.pkl', 'wb')
pickle.dump(user_id_map, output)

