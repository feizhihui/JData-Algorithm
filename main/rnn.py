# encoding=utf-8

import tensorflow as tf
import numpy as np

num_steps = 400
feature_size = 7
learning_rate = 0.002
hidden_size = 128
num_layers = 1
output_size = 2
init_scale = 0.1


class BiRNN:
    def __init__(self, batch_size):
        initializer = tf.random_uniform_initializer(-init_scale, init_scale)
        with tf.variable_scope("jd-model", reuse=None, initializer=initializer):
            self.inputs = tf.placeholder(tf.float32, [batch_size, num_steps, feature_size])
            self.targets = tf.placeholder(tf.int32, [batch_size])
            self.sequence_lengths = tf.placeholder(tf.int32, shape=[batch_size])
            self.mask_weight = tf.placeholder(tf.float32, shape=[batch_size])
            self.keep_prob = tf.placeholder(tf.float32)

            lstm_cell = tf.contrib.rnn.BasicLSTMCell(hidden_size, forget_bias=0.0, state_is_tuple=True)
            lstm_cell = tf.contrib.rnn.DropoutWrapper(lstm_cell, output_keep_prob=self.keep_prob)
            lstm_net = tf.contrib.rnn.MultiRNNCell([lstm_cell] * num_layers, state_is_tuple=True)
            #  (n,num_steps,hidden_size)
            outputs, state = tf.nn.dynamic_rnn(lstm_net, self.inputs, sequence_length=self.sequence_lengths,
                                               dtype=tf.float32)
            # output = outputs[:, self.sequence_lengths[i] - 1, :]
            output_list = []
            for i, one_sample in enumerate(tf.unstack(outputs)):
                one_sample = one_sample[self.sequence_lengths[i] - 1]
                output_list.append(one_sample)
            output = tf.stack(output_list)

            softmax_w = tf.get_variable("softmax_w", [hidden_size, output_size], dtype=tf.float32)
            softmax_b = tf.get_variable("softmax_b", [output_size], dtype=tf.float32)
            # logits shape is (n,2)
            self.logits = tf.nn.softmax(tf.matmul(output, softmax_w) + softmax_b)
            self.prediction = tf.argmax(self.logits, axis=1)
            entropy_loss = -tf.reduce_sum(tf.one_hot(self.targets, 2) * tf.log(self.logits), axis=1)
            self.mean_loss = 100.0 * tf.reduce_mean(entropy_loss * self.mask_weight)
            self.optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(self.mean_loss)

    def propagation(self, sess, batch_x, batch_y, batch_lens, keep_prob):
        tw, fw = 1, 2.54
        mask_weight = np.select([batch_y == 0, batch_y == 1], [fw / (tw + fw), tw / (tw + fw)])
        feed_dict = {self.inputs: batch_x, self.targets: batch_y, self.sequence_lengths: batch_lens,
                     self.keep_prob: keep_prob, self.mask_weight: mask_weight}
        prediction, mean_loss, _ = sess.run([self.prediction, self.mean_loss, self.optimizer], feed_dict=feed_dict)
        return prediction, mean_loss

    def referrence(self, sess, batch_x, batch_lens, keep_prob=1.):
        feed_dict = {self.inputs: batch_x, self.sequence_lengths: batch_lens,
                     self.keep_prob: keep_prob}
        prediction = sess.run(self.prediction, feed_dict=feed_dict)
        return prediction

    def referrence_logits(self, sess, batch_x, batch_lens, keep_prob=1.):
        feed_dict = {self.inputs: batch_x, self.sequence_lengths: batch_lens,
                     self.keep_prob: keep_prob}
        logits = sess.run(self.logits, feed_dict=feed_dict)
        return logits[:, 1]

    def propagation_logits(self, sess, batch_x, batch_y, batch_lens, keep_prob):
        tw, fw = 1, 1
        mask_weight = np.select([batch_y == 0, batch_y == 1], [fw / (tw + fw), tw / (tw + fw)])
        feed_dict = {self.inputs: batch_x, self.targets: batch_y, self.sequence_lengths: batch_lens,
                     self.keep_prob: keep_prob, self.mask_weight: mask_weight}
        logits, mean_loss, _ = sess.run([self.logits, self.mean_loss, self.optimizer], feed_dict=feed_dict)
        return logits[:, 1], mean_loss
