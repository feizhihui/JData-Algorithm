# encoding=utf-8
import pickle
import time
import random

sampled_num = 0

num_steps = 400

output = open('DATA/label04_map.pkl', 'rb')
label04_map = pickle.load(output)

start_time = time.time()
file = open('DATA/actionMap03.pkl', mode='rb')
action_map = pickle.load(file)

output = open('DATA/user_id_map.pkl', 'rb')
user_id_map = pickle.load(output)
total_user = len(user_id_map)
print('load operation finished!')

print('before oversampleing:')
print('no pay user', total_user - len(label04_map))
print('pay user', len(label04_map))


def over_sampling(user, action_list):
    global sampled_num
    size = len(action_list)
    step = max(1, size // 84)
    for i in range(0, size // 2 - 1, step):
        user_sample = user + '_' + str(i)
        assert len(user) == 6
        shu_list = action_list[i:i + size // 84]
        random.shuffle(shu_list)
        action_list = action_list[:i] + shu_list + action_list[i + size // 84:]
        action_map2[user_sample] = action_list
        label04_map[user_sample] = label04_map[user]
        user_id_map[user_sample] = total_user + sampled_num

        sampled_num += 1


print(time.time() - start_time)
count = 0
action_map2 = {}
for user, action_list in action_map.items():
    user = user[:-2]
    action_map2[user] = action_list[-num_steps:]
    print('%d ,-- %d' % (count, len(action_map2[user])))
    count += 1
    if user in label04_map:
        over_sampling(user, action_map2[user])

print('sampled_num', sampled_num)

print('no pay user', total_user + sampled_num - len(label04_map))
print('pay user', len(label04_map))

file = open('DATA/actionMap_beta_sam.pkl', mode='wb')
pickle.dump(action_map2, file)

file = open('DATA/label04_map_beta.pkl', mode='wb')
pickle.dump(label04_map, file)
file = open('DATA/user_id_map_beta.pkl', mode='wb')
pickle.dump(user_id_map, file)

print(time.time() - start_time)
