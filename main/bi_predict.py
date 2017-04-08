# encoding=utf-8
import time
import data_input
import tensorflow as tf
import rnn
import numpy as np
import pickle

epoch_num = 2
batch_size = 128
keep_probs = 1.0

start_time = time.time()
jd = data_input.JData()

model = rnn.BiRNN(batch_size)
total_iters = jd.total_user * epoch_num // batch_size
print('total iterations are', total_iters)


# mask sample effect
def calculate_score2(output, label, user_selected, id2user):
    accuracy = np.sum(np.equal(output, label)) / batch_size

    mask = np.zeros_like(label)
    for i in range(len(user_selected)):
        user = id2user[user_selected[i]]
        if len(user) > 6 and user[6] == '_':
            mask[i] = 0
        else:
            mask[i] = 1
    # mask oversample
    for i in range(len(mask)):
        output[i] *= mask[i]
        label[i] *= mask[i]

    accuracy = np.sum(np.equal(output, label)) / batch_size
    TP = np.sum(output * label == 1)
    precision = TP / max(np.sum(output), 1e-12)
    recall = TP / max(np.sum(label), 1e-12)

    if 5 * recall + precision == 0:
        f1_score = 0
    else:
        f1_score = 6 * recall * precision / (5 * recall + precision)
    return accuracy, precision, recall, f1_score


# no mask sample effect
def calculate_score(output, label):
    accuracy = np.sum(np.equal(output, label)) / batch_size
    TP = np.sum(output * label == 1)
    precision = TP / max(np.sum(output), 1e-12)
    recall = TP / max(np.sum(label), 1e-12)
    if 5 * recall + precision == 0:
        f1_score = 0
    else:
        f1_score = 6 * recall * precision / (5 * recall + precision)
    return accuracy, precision, recall, f1_score


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for iter in range(total_iters):
        batch_x, sequence_lengths, user_selected = jd.next_batch(batch_size)
        label = jd.next_label(user_selected)
        output, mean_loss = model.propagation(sess, batch_x, label, sequence_lengths, keep_probs)
        if iter % 20 == 0:
            # if mask oversample
            accuracy, precision, recall, f1_score = calculate_score2(output, label, user_selected, jd.row2user)
            print('=======================================')
            print('Accuracy:%.3f Precision:%.3f Recall:%.3f How many user will pay:%d, Real pay:%d' % (
                accuracy, precision, recall, np.sum(output), np.sum(label)))
            print('iter %d/%d Mean-Loss %.4f , F1-Score: %.4f' % (iter, total_iters, mean_loss, f1_score))

    del jd.action_map
    print('begin to test!')
    jd.read_test_data()
    # row2user changed
    result = jd.next_test_batch(batch_size)
    user_list = []
    iter = 0
    while result != None:
        iter += 1
        if iter % 20 == 0:
            print('finished test', iter)
        batch_x, sequence_lengths, user_selected = result
        prediction = model.referrence(sess, batch_x, sequence_lengths, keep_prob=1.0)
        for i, line in enumerate(prediction):
            if line == 1:
                userid = user_selected[i]
                user_list.append(jd.row2user[userid])
        result = jd.next_test_batch(batch_size)
    print('saved user:', len(user_list))
    file = open('user_list.pkl', 'wb')
    pickle.dump(user_list, file)
