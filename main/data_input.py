# encoding=utf-8
import pickle
import time
import numpy as np

num_steps = 400
action_num = 6


class JData:
    def __init__(self):
        start_time = time.time()
        file = open('../data_utils/DATA/actionMap_beta_sam.pkl', mode='rb')  # if sam, oversampleing
        action_map = pickle.load(file)
        # file = open('../data_utils/DATA/sku_id_map.pkl', mode='rb')
        # sku_id_map = pickle.load(file)
        # file = open('../data_utils/DATA/user_id_map_beta.pkl', mode='rb')  # if beta, oversampleing
        # user_id_map = pickle.load(file)
        file = open('../data_utils/DATA/label04_map_beta.pkl', mode='rb')  # if beta, oversampleing
        label04 = pickle.load(file)

        # self.total_item = total_item = len(action_map)
        # self.total_sku = total_sku = len(sku_id_map)
        total_user = len(action_map)

        sequence_lengths = np.zeros([total_user])
        # one_action=(sku_id, action_type, action_time)
        # shape=[total_user, num_steps, total_sku + action_num + 1] is too big
        data = np.zeros(shape=[total_user, num_steps, action_num + 1])
        row2user = {}
        for rowid, (user, values) in enumerate(action_map.items()):
            # user id in total user set
            row2user[rowid] = user
            sequence_lengths[rowid] = len(values)
            for j, action in enumerate(values):
                # one_action=(sku_id, action_type, action_time)
                # sku_id = int(sku_id_map[action[0]])
                action_type = int(action[1])
                vistit_date = int(action[2])
                # backward padding
                data[rowid, j, action_type - 1] = 1
                data[rowid, j, - 1] = vistit_date

        self.total_user = len(data)
        self.data = data
        self.sequence_lengths = np.array(sequence_lengths)
        self.action_map = action_map
        self.row2user = row2user
        self.label04 = label04
        print('training set lens=', self.total_user)

    def next_batch(self, bath_size):
        user_selected = np.random.randint(self.total_user, size=bath_size)
        return self.data[user_selected], self.sequence_lengths[user_selected], user_selected

    def next_label(self, user_selected):
        label = []
        for user_id in user_selected:
            user = self.row2user[user_id]
            if user in self.label04:
                label.append(1)
            else:
                label.append(0)
        return np.array(label)

    def read_test_data(self):
        file = open('../test/DATA/actionMap04_beta.pkl', mode='rb')
        action_map = pickle.load(file)
        total_user = len(action_map)
        data = np.zeros(shape=[total_user, num_steps, action_num + 1])
        sequence_lengths = np.zeros([total_user])
        row2user = {}
        for rowid, (user, values) in enumerate(action_map.items()):
            # user id in total user set
            row2user[rowid] = user
            # 用户编号转化成用户id
            sequence_lengths[rowid] = len(values)
            for j, action in enumerate(values):
                # one_action=(sku_id, action_type, action_time)
                # sku_id = int(sku_id_map[action[0]])
                action_type = int(action[1])
                vistit_date = int(action[2])
                # backward padding
                data[rowid, j, action_type - 1] = 1
                data[rowid, j, - 1] = vistit_date
        self.data = data
        self.row2user = row2user
        self.sequence_lengths = sequence_lengths
        self.index = 0
        self.total_user = len(data)
        print('testing set lens=', self.total_user)

    def next_test_batch(self, bath_size):
        if self.index + bath_size >= self.total_user:
            return None
        user_selected = range(self.index, self.index + bath_size)
        result = (self.data[user_selected], self.sequence_lengths[user_selected], user_selected)
        self.index += bath_size
        return result
