# encoding=utf-8
import pickle
import time

num_steps = 400

start_time = time.time()
file = open('DATA/actionMap03.pkl', mode='rb')
action_map = pickle.load(file)
print('load operation finished!')
print(time.time() - start_time)
count = 0
action_map2 = {}
for user, action_list in action_map.items():
    user = user[:-2]
    action_map2[user] = action_list[-num_steps:]
    print('%d ,-- %d' % (count, len(action_map2[user])))
    count += 1

file = open('DATA/actionMap03_beta.pkl', mode='wb')
pickle.dump(action_map2, file)

print(time.time() - start_time)
