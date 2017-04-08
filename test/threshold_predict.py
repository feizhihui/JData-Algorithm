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
threshold = 0.2

start_time = time.time()
jd = data_input.JData()

model = rnn.BiRNN(batch_size)
total_iters = jd.maxlen * epoch_num // batch_size
print('total iterations are', total_iters)

id2user = dict(zip(jd.user_id_map.values(), jd.user_id_map.keys()))


def calculate_score2(output, label):
    # output shape is [batch-size,1], 1 on behalf of pay 0 on not
    true_positive = 0
    p_num = 1e-12
    for i, line in enumerate(output):
        if label[i] == 1:
            p_num += 1
            if line == 1:
                true_positive += 1
    precision = true_positive / batch_size
    recall = true_positive / p_num
    if 5 * recall + precision == 0:
        f1_score = 0
    else:
        f1_score = 6 * recall * precision / (5 * recall + precision)
    return precision, recall, f1_score


def calculate_score_logits(logits, label):
    output = (logits > threshold).astype(int)
    accuracy = np.sum(np.equal(output, label)) / batch_size
    TP = np.sum(output * label == 1)
    precision = TP / max(np.sum(output), 1e-12)
    recall = TP / max(np.sum(label), 1e-12)
    if 5 * recall + precision == 0:
        f1_score = 0
    else:
        f1_score = 6 * recall * precision / (5 * recall + precision)
    return output, accuracy, precision, recall, f1_score


with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for iter in range(total_iters):
        batch_x, sequence_lengths, user_selected = jd.next_batch(batch_size)
        label = jd.next_label(user_selected, id2user)
        logits, mean_loss = model.propagation_logits(sess, batch_x, label, sequence_lengths, keep_probs)
        if iter % 20 == 0:
            output, accuracy, precision, recall, f1_score = calculate_score_logits(logits, label)
            print('=======================================')
            print('Accuracy:%.3f Precision:%.3f Recall:%.3f How many user will pay:%d, True pay:%d' % (
                accuracy, precision, recall, np.sum(output), np.sum(label)))
            print('iter %d/%d Mean-Loss %.4f , F1-Score: %.4f' % (iter, total_iters, mean_loss, f1_score))

    print('begin to test!')
    jd.read_test_data()
    result = jd.next_test_batch(batch_size)
    user_list = []
    while result != None:
        batch_x, sequence_lengths, user_selected = result
        logits = model.referrence_logits(sess, batch_x, sequence_lengths, keep_prob=1.0)
        prediction = (logits > threshold).astype(int)
        for i, line in enumerate(prediction):
            if line == 1:
                userid = user_selected[i]
                user_list.append(id2user[userid])
        result = jd.next_test_batch(batch_size)
    print('saved user:', len(user_list))
    file = open('user_list.pkl', 'wb')
    pickle.dump(user_list, file)
