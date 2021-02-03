# pylint: disable-all
# coding: utf-8
import os
import tensorflow as tf
import time
import numpy as np
from sklearn.model_selection import train_test_split
from utils import multi_accuracy, create_batch, k_accuracy, k2_accuracy
from model import M_IRN
from data_utils import process_dataset, MultiKnowledgeBase, KnowledgeBase, recover_predictions

flags = tf.flags

flags.DEFINE_integer("embedding_dimension", 64, "KG vector dimension [50]")
flags.DEFINE_integer("batch_size", 50, "batch size to use during training [50]")
flags.DEFINE_float("max_grad_norm", 10, "clip gradients to this norm [10]")
flags.DEFINE_float("lr", 0.001, "Learning rate [0.001]")
flags.DEFINE_float("epsilon", 1e-8, "Epsilon for Adam Optimizer [1e-8]")
flags.DEFINE_string("dataset", "EN_en_en_fr", "dataset name")
flags.DEFINE_string("checkpoint_dir", "checkpoint", "checkpoint directory")
flags.DEFINE_string("data_dir", "data", "dataset directory")
flags.DEFINE_string("kb_dir", "ideal", "kb and alignment directory")
flags.DEFINE_boolean("direct_align", True, "Replace entity embedding alignment with actual alignment")
flags.DEFINE_boolean("dual_matrices", False, "Whether to use two transfer matrices")
flags.DEFINE_boolean("save", False, "Whether to save predictions in strings")
flags.DEFINE_integer("sentence_size", 0, "")
flags.DEFINE_integer("question_words", 0, "")
flags.DEFINE_integer("hops", 0, "")
flags.DEFINE_integer("this_k_1_2", 0, "")
flags.DEFINE_integer("this_k_2_1", 0, "")
flags.DEFINE_string("lan_que", "", "")
flags.DEFINE_list("lan_labels", [], "")
flags.DEFINE_list("steps", [], "")
flags.DEFINE_integer("top_k", 1, "")

FLAGS = flags.FLAGS


def main(_):
    FLAGS.checkpoint_dir = os.path.join(FLAGS.checkpoint_dir, FLAGS.dataset)
    if not os.path.exists(FLAGS.checkpoint_dir):
        os.makedirs(FLAGS.checkpoint_dir)

    d_labels = FLAGS.dataset.split("_")
    lan_1 = d_labels[1]
    kb1_file = '{}/{}/{}_KB.txt'.format(FLAGS.data_dir, FLAGS.kb_dir, lan_1)
    lan_2 = ""
    for label in d_labels[1:]:
        if label != lan_1:
            lan_2 = label
            break
    kb2_file = '{}/{}/{}_KB.txt'.format(FLAGS.data_dir, FLAGS.kb_dir, lan_2)
    data_file = '{}/{}.txt'.format(FLAGS.data_dir, FLAGS.dataset)

    dir = lan_1 + "_" + lan_2
    is_flip = True if dir in ["zh_fr", "en_fr", "zh_en"] else False

    align_gold_file = '{}/{}/{}_{}_correct.txt'.format(FLAGS.data_dir, FLAGS.kb_dir, lan_2 if is_flip else lan_1,
                                                       lan_1 if is_flip else lan_2)
    align_pred_file_1_2 = '{}/{}/{}_{}_predictions_hits@{}.txt'.format(FLAGS.data_dir, FLAGS.kb_dir, lan_1, lan_2,
                                                                      FLAGS.top_k)
    align_pred_file_2_1 = '{}/{}/{}_{}_predictions_hits@{}.txt'.format(FLAGS.data_dir, FLAGS.kb_dir, lan_2, lan_1,
                                                                      FLAGS.top_k)

    start = time.time()
    print("Loading data...")

    # build and store knowledge bases
    kb1 = KnowledgeBase(kb1_file, name="kb1")
    kb2 = KnowledgeBase(kb2_file, name="kb2")
    multi_kb = MultiKnowledgeBase(kb1, kb2, align_gold_file, is_flip)
    # load predictions from alignment model
    multi_kb.load_pred(align_pred_file_1_2, align_pred_file_2_1)

    q_ids, p_ids, q_strs, p_strs, qw2id, FLAGS.sentence_size, FLAGS.question_words, FLAGS.hops, \
    FLAGS.lan_que, FLAGS.lan_labels, FLAGS.steps = process_dataset(data_file, multi_kb)

    print("Data loading cost {} seconds".format(time.time() - start))

    train_q, test_q, train_p, test_p = train_test_split(q_ids, p_ids, test_size=.1, random_state=123)

    n_testing = test_q.shape[0]
    print("Testing Size", n_testing)

    t_batches = create_batch(n_testing, FLAGS.batch_size)


    if FLAGS.direct_align:
        with tf.Session() as sess:
            model = M_IRN(FLAGS, multi_kb, sess)
            model.load()
            t_preds = model.predict(test_q, test_p, t_batches)
            t_accu, t_al, t_strict = multi_accuracy(test_p, t_preds, multi_kb, FLAGS.steps, FLAGS.hops, FLAGS.lan_labels)
            if FLAGS.save:
                recov_name = data_file.strip(".txt") + "_predictions.txt"

            print('-----------------------')
            print('Test is under direct align mode.')
            print('Test Data', data_file)
            print('Test Accuracy:', t_accu, t_al)
            print("Strict test accuracy: ", t_strict)
            if FLAGS.save:
                print("prediction results saved in {}.".format(recov_name))
                recover_predictions(recov_name, t_preds, multi_kb, FLAGS.hops, FLAGS.lan_labels, FLAGS.steps)
            print('-----------------------')

    else:
        if FLAGS.steps[-1] < 8 or FLAGS.top_k == 1:
            t_preds_k = []
            for k in range(FLAGS.top_k):
                FLAGS.this_k_1_2 = FLAGS.this_k_2_1 = k
                print('Building model for top {}...'.format(k + 1))
                with tf.Session() as sess:
                    model = M_IRN(FLAGS, multi_kb, sess)
                    model.load()
                    print('Predicting top {}...'.format(k+1))
                    t_preds_k.append(model.predict(test_q, test_p, t_batches))
                tf.reset_default_graph()
            t_preds_k = np.array(t_preds_k)
            path_accu, strict_accu = k_accuracy(test_p, t_preds_k)
            print('-----------------------')
            print('Test is under align prediction with hits@{} mode(with only one alignment).'.format(FLAGS.top_k))
            print('Test Data', data_file)
            print('Test Path Accuracy:', path_accu)
            print("Strict test accuracy: ", strict_accu)
            print('-----------------------')

        else:
            t_preds_k = []
            for k in range(FLAGS.top_k):
                for j in range(FLAGS.top_k):
                    FLAGS.this_k_1_2 = k
                    FLAGS.this_k_2_1 = j
                    print('Building model for top {} + top {}...'.format(k + 1, j + 1))
                    with tf.Session() as sess:
                        model = M_IRN(FLAGS, multi_kb, sess)
                        model.load()
                        print('Predicting top {} + top {}...'.format(k + 1, j + 1))
                        t_preds_k.append(model.predict(test_q, test_p, t_batches))
                    tf.reset_default_graph()
            t_preds_k = np.array(t_preds_k)
            path_accu, strict_accu = k2_accuracy(test_p, t_preds_k, multi_kb)
            print('-----------------------')
            print('Test is under align prediction with hits@{} mode(with two alignments).'.format(FLAGS.top_k))
            print('Test Data', data_file)
            print('Test Path Accuracy:', path_accu)
            print("Strict test accuracy: ", strict_accu)
            print('-----------------------')


if __name__ == '__main__':
    tf.app.run(main)
