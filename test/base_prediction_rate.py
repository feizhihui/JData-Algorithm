# encoding=utf-8
import pickle


def cal_max_score(values):
    # 1浏览 2加入购物车 3删除 4下单 5关注 6点击
    score = {'1': 2, '2': 8, '3': -10, '4': -10, '5': 5, '6': 1}
    score_table = {}
    for v in values:
        item = v[0]
        action = v[1]
        if item in score_table:
            score_table[item] += score[action]
        else:
            score_table[item] = score[action]
    new_score = sorted(score_table.items(), key=lambda x: x[1], reverse=True)
    return new_score[0]


file = open('DATA/actionMap04_beta.pkl', 'rb')
actionMap = pickle.load(file)

print('action lens:', len(actionMap))

result = {}
for user, action_list in actionMap.items():
    values = actionMap[user]
    item = cal_max_score(values)
    if item[1] > 0:
        result[user] = item[0]

print('submit result', len(result))

file = open('result.csv', 'w')
file.write('user_id,sku_id\n')
for user, item in result.items():
    file.write(user + ',' + item + '\n')
file.close()
