# coding: utf-8
import numpy as np
import tensorflow as tf
from sklearn import metrics
from data_utils import MultiKnowledgeBase
from math import sqrt


def norm(matrix):
    '''Matrix normalization'''
    n = tf.sqrt(tf.reduce_sum(matrix * matrix, 1))
    return tf.reshape(n, [-1, 1])


def MatrixCos(inputdata, key):
    '''inputdata = [batch,embed]
        key = [slot,embed]
    return most similar key_id for each inputdata'''
    addressing = tf.matmul(inputdata, key, transpose_b=True)  # (b,e)*(e,slots) -> (b,s)
    norm1 = norm(inputdata)  # (b,1)
    norm2 = norm(key)  # (s,1)
    n = tf.matmul(norm1, norm2, transpose_b=True) + 1e-8  # (b,s)
    addressing = tf.div(addressing, n)
    index = tf.reshape(tf.argmax(addressing, 1), [-1, 1])  # (b,1)
    return tf.to_int32(index)


def SimpleMatrixCos(inputdata, key):
    inputdata = tf.nn.l2_normalize(inputdata, 1)
    key = tf.nn.l2_normalize(key, 1)
    addressing = tf.matmul(inputdata, key, transpose_b=True)  # (b,4)*(4,5) -> (b,5)
    index = tf.reshape(tf.argmax(addressing, 1), [-1, 1])  # (b,1)
    return tf.to_int32(index)


def position_encoding(sentence_size, embedding_size):
    """
    Position Encoding described in section 4.1 [1]
        m_i = sum_j l_ij*A*x_ij /J/d
        l_ij = Jd-jd-iJ+2ij  = ij-Ji/2-jd/2+Jd/4
    return l-matrix-transpose (fixed)
    """
    encoding = np.ones((embedding_size, sentence_size), dtype=np.float32)
    ls = sentence_size + 1
    le = embedding_size + 1
    for i in range(1, le):
        for j in range(1, ls):
            encoding[i - 1, j - 1] = (i - (le - 1) / 2) * (j - (ls - 1) / 2)
    encoding = (1 + 4 * encoding / embedding_size / sentence_size) / 2
    return np.transpose(encoding)


def add_gradient_noise(t, stddev=1e-3, name=None):
    """
    Adds gradient noise as described in http://arxiv.org/abs/1511.06807 [2].

    The input Tensor `t` should be a gradient.

    The output will be `t` + gaussian noise.

    0.001 was said to be a good fixed value for memory networks [2].
    """
    with tf.name_scope(name, "add_gradient_noise", [t, stddev]) as name:
        t = tf.convert_to_tensor(t, name="t")
        gn = tf.random_normal(tf.shape(t), stddev=stddev)
        return tf.add(t, gn, name=name)


def zero_nil_slot(t, name=None):
    """
    Overwrites the nil_slot (first row) of the input Tensor with zeros.
    The nil_slot is a dummy slot and should not be trained and influence
    the training algorithm.
    """
    with tf.name_scope(name, "zero_nil_slot", [t]) as name:
        t = tf.convert_to_tensor(t, name="t")
        s = tf.shape(t)[1]
        z = tf.zeros(tf.stack([1, s]))  # tf.zeros([1,s])
        return tf.concat(axis=0, values=[z, tf.slice(t, [1, 0], [-1, -1])], name=name)


def multi_accuracy(labels: np.ndarray, predictions: np.ndarray, multi_base: MultiKnowledgeBase, steps: list,
                   hops, lan_labels):
    # compare path and final answer accuracy
    accuracies = []

    for i in range(steps[-1]+1):
        accuracies.append("{:.3f}".format(round(metrics.accuracy_score(labels[:, i], predictions[:, i]), 3)))

    align_dict_1_2 = multi_base.align_dict_1_2
    align_dict_2_1 = multi_base.align_dict_2_1
    align_accuracies = "Alignment accuracy on reasoning:"
    for i in range(hops - 1):
        if lan_labels[i + 1] != lan_labels[i]:
            if lan_labels[i + 1] == lan_labels[0]:
                anf = 0
                alignment_labels = []
                for ent_id in predictions[:, steps[i+1]].tolist():
                    if ent_id in align_dict_2_1.keys():
                        alignment_labels.append(align_dict_2_1[ent_id])
                    else:
                        alignment_labels.append(0)
                        anf += 1
                aligned_ids = predictions[:, steps[i+1]+1].tolist()
                l = len(alignment_labels)
                align_accuracies += "\nAlign miss rate 2-1: " + str(round(anf / l, 3))
                a = 0
                for i in range(l):
                    if alignment_labels[i] != 0:
                        if alignment_labels[i] == aligned_ids[i]:
                            a += 1
                    else:
                        l -= 1
                align_accuracies += ", Align accuracy 2-1: " + (str(round(a / l, 3)) if l > 0 else str(0))
            else:
                anf = 0
                alignment_labels = []
                for ent_id in predictions[:, steps[i+1]].tolist():
                    if ent_id in align_dict_1_2.keys():
                        alignment_labels.append(align_dict_1_2[ent_id])
                    else:
                        alignment_labels.append(0)
                        anf += 1
                aligned_ids = predictions[:, steps[i+1]+1].tolist()
                l = len(alignment_labels)
                align_accuracies += "\nAlign miss rate 1-2: " + str(round(anf / l, 3))
                a = 0
                for i in range(l):
                    if alignment_labels[i] != 0:
                        if alignment_labels[i] == aligned_ids[i]:
                            a += 1
                    else:
                        l -= 1
                align_accuracies += ", Align accuracy 1-2: " + (str(round(a / l, 3)) if l > 0 else str(0))

    pl = steps[-1]+1
    tl = len(labels)
    cr = 0

    for i in range(tl):
        correct = True
        for j in range(pl):
            correct = labels[i, j] == predictions[i, j]
            if not correct:
                break
        if correct:
            cr+=1
    accu_strict = cr/float(tl)

    return accuracies, align_accuracies, "{:.3f}".format(accu_strict)

def accuracy_w_res_arr(res_arr):
    path_accuracy = []
    for m in range(res_arr.shape[1]):
        step_preds = res_arr[:, m]
        path_accuracy.append("{:.3f}".format(step_preds.sum() / step_preds.shape[0]))

    cr = 0
    for path in res_arr:
        correct = True
        for step in path:
            if step == 0:
                correct = False
                break
        if correct:
            cr += 1
    accu_strict = "{:.3f}".format(cr / res_arr.shape[0])

    return path_accuracy, accu_strict

def k_accuracy(labels: np.ndarray, preds_k:np.ndarray):
    # preds_k shape is (k, n, p)
    k = preds_k.shape[0]
    res_arr = np.zeros(preds_k[0].shape)
    for i in range(k):
        preds = preds_k[i]
        for p in range(len(preds)):
            path = preds[p]
            for s in range(len(path)):
                if path[s] == labels[p][s]:
                    res_arr[p][s] = 1
    return accuracy_w_res_arr(res_arr)

def k2_accuracy(labels: np.ndarray, preds_k2:np.ndarray,  multi_base: MultiKnowledgeBase):
    # (k2, n, p)
    sc_dict_1_2 = multi_base.score_dict_1_2
    sc_dict_2_1 = multi_base.score_dict_2_1
    k2 = preds_k2.shape[0]
    k = int(sqrt(k2))
    res_arr = np.zeros(preds_k2[0].shape)
    p_l = preds_k2.shape[2]
    align_miss = 0
    for n in range(preds_k2.shape[1]):
        k2_pool = preds_k2[:, n]
        pool_w_sc = []
        for p in range(k2):
            path = k2_pool[p]
            score_product = sc_dict_1_2[(path[2], path[3])] * sc_dict_2_1[(path[5], path[6])]
            pool_w_sc.append((k2_pool[p], score_product))
            if path[3] == -1 or path[6] == -1:
                align_miss += 1
        sorted_pool = sorted(pool_w_sc, key = lambda x: x[1], reverse=True)
        top_k = np.squeeze(np.delete(sorted_pool, -1, 1).tolist())[:k]
        for i in range(k):
            path = top_k[i]
            for j in range(p_l):
                if path[j] == labels[n][j]:
                    res_arr[n][j] = 1
    print('Align miss: {}'.format(align_miss))

    return accuracy_w_res_arr(res_arr)

def create_batch(instances, batch_size):
    s = list(zip(range(0, instances - batch_size, batch_size), range(batch_size, instances, batch_size)))
    if instances % batch_size != 0:
        s.append(((instances - instances % batch_size, instances)))
    else:
        s.append((instances - batch_size, instances))
    return s


def orthogonal(shape):
  flat_shape = (shape[0], np.prod(shape[1:]))
  a = np.random.normal(0.0, 1.0, flat_shape)
  u, _, v = np.linalg.svd(a, full_matrices=False)
  q = u if u.shape == flat_shape else v
  return q.reshape(shape)


def orthogonal_initializer(scale=1.0, dtype=tf.float32):
  def _initializer(shape, dtype=tf.float32, partition_info=None):
    return tf.constant(orthogonal(shape) * scale, dtype)
  return _initializer