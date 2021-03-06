import os
import sys
sys.path.append("..")
import yaml
import tensorflow as tf
import numpy as np


def test_placeholder():
    """
    test whether int type placeholder can be an indice of a list 
    """
    task = tf.placeholder(tf.int32)

    l = [0] * len(params["task"])
    l[task] = 1  # list indices must be integers not tensor

    task_label = tf.constant(l, dtype=tf.float32)
    task_label = tf.expand_dims(task_label, 0)

    with tf.Session() as sess_1:
        feed_dict = {
            task: 1
        }
        with tf.Session() as sess:
            indice = sess.run(
                task, feed_dict=feed_dict
            )
            print(indice)


def test_initialize():
    a = tf.Variable(tf.truncated_normal(
        [100, 5], stddev=0.1), name="W1")
    i = tf.placeholder(tf.int32)

    with tf.Session() as sess:
        feed_dict = {i: 1}
        indice = sess.run(i, feed_dict=feed_dict)
    return indice


def test_tf_gather():
    a = tf.constant([1, 2, 4, 2, 4, 1, 2, 5])
    indice = tf.placeholder(tf.int32)
    b = tf.gather(a, indices=indice)

    with tf.Session() as sess:
        a, b = sess.run([a, b], feed_dict={indice: 3})
        print(a)
        print(b)


def test_tf_gather_v2():
    l = ["sehe", "srghuiheg", "serh", "erh", "erbhi"]
    indice = tf.placeholder(tf.int32)
    res = tf.gather(l, indice)
    name_scope = "wegwuahv{}".format(res)
    with tf.Session() as sess:
        res_, ns = sess.run([res, name_scope], feed_dict={indice: 3})
        print(res_)
        print(ns)
    pass


def test_assign():
    l = [1, 3, 5, 6]
    ref = tf.constant(l, dtype=tf.int32)
    indice = tf.placeholder(tf.int32)
    select = tf.gather(ref, indice)
    tf.assign(select, value=1)
    pass


def test_one_hot():
    indice = tf.placeholder(tf.int32)
    l = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ret = tf.one_hot(indice, len(l))
    ret = tf.expand_dims(ret, 0)
    ret = tf.tile(ret, [10, 1])
    with tf.Session() as sess:
        ret_ = sess.run(ret, feed_dict={indice: 4})
        print(ret_)


def gen_batch(data):
    """
    """

    l3 = [8, 4, 3, 2, 1, 6, 5, 3, 1, 6, 5, 6]

    for batch in zip(l3, data):
        yield batch


def test_yield():
    l1 = [1, 2, 4, 6, 7, 5, 6, 8, 8, 6, 1, 6]
    l2 = [2, 3, 6, 5, 2, 3, 6, 8, 2, 3, 6, 6]
    data = zip(l1, l2)
    for batch in gen_batch(data):
        print(batch)


def test_batch():
    import random
    d = [
        [
            "efga wgw haivaw",
            "a wu fh wuh wav",
            "avd hu hwwe wVW",
            "EE VHE AV EAB"
        ],
        [
            "6347 8346 T37",
            "2758 2755 3 5EG"
        ],
        [
            "e g u i",
            "v h",
            "s e r h"
        ]
    ]
    l = [
        [
            0,
            1,
            0,
            1
        ],
        [
            1,
            1
        ],
        [
            0,
            1,
            0
        ]

    ]

    data = []
    for i in range(len(d)):
        data.append(list(zip(d[i], l[i])))

    for i in range(10):
        task = random.randint(0, 2)
        yield task, data[task]


def test_batch_iter():
    for task, batch in test_batch():
        print(task)
        print(batch)
        x, y = zip(*batch)
        print(x, y)
        print("############")
    pass


def test_cond():
    a = tf.constant(10)
    b = tf.constant(20)
    indice = tf.placeholder(tf.int32)

    def f1():
        return a

    def f2():
        return 0
    res = tf.cond(tf.equal(indice, 0), true_fn=f1, false_fn=f2)
    with tf.Session() as sess:
        res_ = sess.run(res, feed_dict={indice: 0})
        print(res_)
        pass
    pass


def test_cond_for():
    indice = tf.placeholder(tf.int32)
    a = tf.constant([2, 1, 5, 3, 3, 2, 1, 4, 6, 2, 1], dtype=tf.int32)
    b = tf.constant([0]*11, dtype=tf.int32)
    #p = tf.Variable([0,1,0,0,1,0,1,0,1,0,1], dtype=tf.int32)

    def fn1():
        #tf.assign(p, a)
        return tf.constant([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=tf.int32)

    def fn2():
        #p = tf.assign(p, a)
        return a
    l = []
    for i in range(10):
        temp = tf.cond(tf.equal(indice, i), lambda: a, lambda: b)
        l.append(temp)

    p = tf.gather(l, indice)

    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        l_, res = sess.run([l, p], feed_dict={indice: 5})
        print(l_)
        print(res)

# need to test embedding_layer
# it seemed all bug occured in embedding_layer
# or maybe it is caused by processor test processor.Vocabulary_


def test_vocabulary():
    from tensorflow.contrib import learn
    processor = learn.preprocessing.VocabularyProcessor.restore(
        "../temp/vocab")

    print(len(processor.vocabulary_))  # get 6877

    file_wv = "../data/glove.6B/glove.6B.{}d.txt".format(100)
    wv = {}
    embedding_matrix = []

    with open(file_wv, 'r') as f:
        for line in f:
            line = line.split(' ')
            word = line[0]
            wv[word] = list(map(float, line[1:]))

    for idx in range(len(processor.vocabulary_)):
        word = processor.vocabulary_.reverse(idx)
        embedding_matrix.append(
            wv[word] if word in wv else np.random.normal(size=100))
    em = np.array(embedding_matrix)
    print(np.shape(em))  # 6877 100 no problem


def test_norm():
    s = [
        [1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2],
        [3, 3, 3, 3, 3],
    ]

    p = [
        [4, 4, 4, 4, 4],
        [5, 5, 5, 5, 5],
        [6, 6, 6, 6, 6]
    ]

    ts = tf.constant(s, dtype=tf.float32)
    tp = tf.constant(p, dtype=tf.float32)
    temp = tf.matmul(ts, tp, transpose_a=True)
    res = tf.norm(temp, ord=2)

    r = [1, 2, 3]

    t = [4, 5, 6]

    tr = tf.constant(r, dtype=tf.float32)
    tt = tf.constant(t, dtype=tf.float32)
    temp1 = tf.matmul(tr, tt, transpose_a=True)
    res1 = tf.norm(temp1, ord=2)

    with tf.Session() as sess:
        temp_, res_ = sess.run([temp1, res1])
        print(temp_)
        print(res_)  # 160
        print(np.shape(temp_))
        print(np.shape(res_))


def test_tensordot():
    s = [
        [1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2],
        [3, 3, 3, 3, 3],
    ]

    p = [
        [4, 4, 4, 4, 4],
        [5, 5, 5, 5, 5],
        [6, 6, 6, 6, 6]
    ]

    ts = tf.constant(s, dtype=tf.float32)
    # ts = tf.expand_dims(ts, axis=1)
    print(ts)
    tp = tf.constant(p, dtype=tf.float32)
    # tp = tf.expand_dims(tp, axis=1)
    # res = tf.tensordot(ts, tp, axes=[[1], [1]])
    temp = tf.multiply(ts, tp)
    temp1 = tf.norm(temp, ord=2, axis=1)
    res = tf.reduce_mean(temp1)
    print(res)
    with tf.Session() as sess:
        res_ = sess.run(res)
        print(res_)


def test_basic_matmul():
    a = tf.constant([0.9, 0.1, 0.2], dtype=tf.float32)
    b = tf.constant([0.1, 0.8, 0.4], dtype=tf.float32)
    res = tf.multiply(a, b)
    # a = tf.expand_dims(a, axis=0)
    # b = tf.expand_dims(b, axis=0)
    # res = tf.matmul(a, b, transpose_a=True)
    res_norm = tf.norm(res, ord=2)
    with tf.Session() as sess:
        res_, rn = sess.run([res, res_norm])
        print(res_, rn)


def test_vocabulary_processor():
    from tensorflow.contrib import learn
    import sys
    sys.path.append("..")
    from utils.data_loader import load_data, batch_iter
    processor = learn.preprocessing.VocabularyProcessor.restore(
        "../temp/vocab")
    processor.max_document_length = 100
    data, label = load_data("test")
    test_data = []
    for d, l in zip(data, label):
        # for each task in data
        d = list(processor.transform(d))  # generator -> list
        d = np.array(d)
        l = np.array(l)
        print(np.shape(d))
        print(np.shape(l))
        test_data.append(d)
    td = np.array(test_data[2])
    print(np.shape(td))

    for task, batch in batch_iter(test_data, label, 7, 3, False):
        x, y = zip(*batch)
        print(task)
        break


def test_get_collections_of_rnn():
    import sys
    sys.path.append("..")
    from model.rnn_model import RNN
    from tensorflow.contrib.rnn import GRUCell
    with tf.variable_scope("rnn-model"):
        # rnn = RNN(
        #     sequence_length=10,
        #     hidden_size=10,
        #     num_layers=1,
        #     dynamic=True,
        #     use_attention=False,
        #     attention_size=10)
        gru = GRUCell(10)
        # 是不是必须要运行之后才可以显示前缀的名字

    rnn_vars = tf.get_collection(
        tf.GraphKeys.TRAINABLE_VARIABLES, scope="rnn-model")
    print(rnn_vars)
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        rv = sess.run(rnn_vars)
        print(rv)


def test_variable_slice():
    """
    tf.Variable can be silced ?
    """
    w = tf.Variable(tf.truncated_normal(
        [6, 3], stddev=0.1), name="w")

    w2 = w[:3]
    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        sess.run(init)
        sw, sw2 = sess.run([w, w2])
        print(sw)
        print(sw2)


def test_relu():
    a = tf.constant([
        [0.9, 0.1, 0.2],
        [1.0, 0.2, -0.4]
    ],
        dtype=tf.float32)
    b = tf.constant([
        [0.0, -0.8, 0.4],
        [0.3, 0.4, 0.5]],
        dtype=tf.float32)

    c = tf.multiply(a, b)

    d = tf.nn.relu(c)

    e = tf.norm(d, ord=2, axis=1)
    f = tf.reduce_mean(e)

    with tf.Session() as sess:
        c_, d_, e_, f_ = sess.run([c, d, e, f])
        print(c_)
        print(d_)
        print(e_)
        print(f_)

def test_random():
    import random
    for j in range(100):        
        if random.randint(0, 20) != 0:
            continue
        
        print("hah")
    pass

def test_assign_variable():
    """
    this test shows assign op can assign value from a tensorflow tensor from a graph
    and from a python object 
    """
    a = tf.Variable(tf.random_uniform([5, 7], -1.0, 1.0), name="a")
    b = tf.Variable(tf.random_uniform([5, 7], -1.0, 1.0), name="b")
    c = np.random.rand(5, 7)

    op1 = b.assign(c)
    op2 = a.assign(b)

    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        print(c)
        print(type(c))
        sess.run(op1)
        print(sess.run(b))
        sess.run(op2)
        print(sess.run(a))
            

if __name__ == "__main__":
    # test_placeholder()
    # res = test_initialize()
    # print(res)

    # test_batch_iter()
    # test_tf_gather_v2()
    # test_one_hot()
    # test_cond()
    # test_cond_for()
    # test_vocabulary()
    # test_norm()
    # test_tensordot()
    # test_basic_matmul()
    # test_vocabulary_processor()
    # test_get_collections_of_rnn()
    # test_variable_slice()
    # test_relu()
    # test_random()
    test_assign_variable()
