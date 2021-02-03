# pylint: disable-all
# coding: utf-8
import os
import tensorflow as tf
import numpy as np
import time
from sklearn.model_selection import train_test_split
from utils import multi_accuracy, create_batch
from model import M_IRN
from data_utils import process_dataset, MultiKnowledgeBase, KnowledgeBase

flags = tf.flags

flags.DEFINE_integer("embedding_dimension", 64, "KG vector dimension [64]")
flags.DEFINE_integer("batch_size", 50, "batch size to use during training [50]")
flags.DEFINE_integer("r_epoch", 2000, "number of epochs to use during training [2000]")
flags.DEFINE_integer("e_epoch", 3, "number of middle epochs for embedding training [3]")
flags.DEFINE_float("max_grad_norm", 20, "clip gradients to this norm [10]")
flags.DEFINE_float("lr", 0.001, "Learning rate [0.001]")
flags.DEFINE_float("epsilon", 1e-8, "Epsilon for Adam Optimizer [1e-8]")
flags.DEFINE_string("dataset", "EN_en_zh_en", "dataset name")
flags.DEFINE_string("checkpoint_dir", "checkpoint", "checkpoint directory")
flags.DEFINE_string("data_dir", "data", "dataset directory")
flags.DEFINE_string("kb_dir", "ideal", "kb and alignment directory")
flags.DEFINE_boolean("resume", False, "Whether to resume last time's training")
flags.DEFINE_boolean("direct_align", True, "Replace entity embedding alignment with actual alignment")
flags.DEFINE_boolean("dual_matrices", False, "Whether to use two transfer matrices")
flags.DEFINE_boolean("pre_kg", False, "Whether to train KG and alignment additionally before reasoning")
flags.DEFINE_integer("sentence_size", 0, "")
flags.DEFINE_integer("question_words", 0, "")
flags.DEFINE_integer("hops", 0, "")
flags.DEFINE_string("lan_que", "", "")
flags.DEFINE_list("lan_labels", [], "")
flags.DEFINE_list("steps", [], "")

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
	is_flip =  True if dir in ["zh_fr", "en_fr", "zh_en"] else False

	align_gold_file = '{}/{}/{}_{}_correct.txt'.format(FLAGS.data_dir, FLAGS.kb_dir, lan_2 if is_flip else lan_1,
	                                               lan_1 if is_flip else lan_2)

	start = time.time()
	print("Loading data...")

	# build and store knowledge bases
	kb1 = KnowledgeBase(kb1_file, name="kb1")
	kb2 = KnowledgeBase(kb2_file, name="kb2")
	multi_kb = MultiKnowledgeBase(kb1, kb2, align_gold_file, is_flip)

	q_ids, p_ids, q_strs, p_strs, qw2id, FLAGS.sentence_size, FLAGS.question_words, FLAGS.hops, \
	FLAGS.lan_que, FLAGS.lan_labels, FLAGS.steps = process_dataset(data_file, multi_kb)

	print("Data loading cost {} seconds".format(time.time() - start))

	train_q, test_q, train_p, test_p = train_test_split(q_ids, p_ids, test_size=.1, random_state=123)
	train_q, valid_q, train_p, valid_p = train_test_split(train_q, train_p, test_size=.11, random_state=0)

	n_training = train_q.shape[0]
	n_testing = test_q.shape[0]
	n_validation = valid_q.shape[0]

	print("Training Size", n_training)
	print("Validation Size", n_validation)
	print("Testing Size", n_testing)

	# batch_id
	# batches = [(start, end) for start, end in batches] abandon last few examples
	tr_batches = create_batch(n_training, FLAGS.batch_size)
	tr_batches_test = create_batch(n_training, FLAGS.batch_size)
	v_batches =  create_batch(n_validation, FLAGS.batch_size)
	t_batches =  create_batch(n_testing, FLAGS.batch_size)

	kb1_triples = multi_kb.kb1.triples
	kb2_triples = multi_kb.kb2.triples

	with tf.Session() as sess:
		model = M_IRN(FLAGS, multi_kb, sess)

		if FLAGS.resume:
			model.load()

		print("knowledge base 1 size", kb1_triples.shape[0])
		print("knowledge base 2 size", kb2_triples.shape[0])
		kg1_embedding_batches =  create_batch(kb1_triples.shape[0], FLAGS.batch_size)
		kg2_embedding_batches = create_batch(kb2_triples.shape[0], FLAGS.batch_size)
		pre_v_preds = model.predict(valid_q, valid_p, v_batches)
		pre_t_preds = model.predict(test_q, test_p, t_batches)
		best_v_ep = -1
		best_v_pa, best_v_al, best_v_ast = multi_accuracy(valid_p, pre_v_preds, multi_kb, FLAGS.steps, FLAGS.hops, FLAGS.lan_labels)
		best_t_pa, best_t_al, best_t_ast = multi_accuracy(test_p, pre_t_preds, multi_kb, FLAGS.steps, FLAGS.hops, FLAGS.lan_labels)

		for t in range(1, FLAGS.r_epoch + 1):

			if t - best_v_ep > 50:
				break

			start = time.time()
			np.random.shuffle(tr_batches)

			kg1_embedding_cost = kg2_embedding_cost = 0.0

			print("MIRN multi epoch {} training...".format(t))

			# e_epoch = 100 if t == 1 else FLAGS.e_epoch

			for i in range(1, FLAGS.e_epoch + 1):
				np.random.shuffle(kg1_embedding_batches)
				np.random.shuffle(kg2_embedding_batches)
				kg1_embedding_total_cost = 0.0
				kg2_embedding_total_cost = 0.0
				for s, e in kg1_embedding_batches:
					kg1_embedding_total_cost += model.batch_train_kg1_embedding(kb1_triples[s:e])
				kg1_embedding_cost = kg1_embedding_total_cost
				for s, e in kg2_embedding_batches:
					kg2_embedding_total_cost += model.batch_train_kg2_embedding(kb2_triples[s:e])
				kg2_embedding_cost = kg2_embedding_total_cost

			reasoning_total_cost = 0.0
			for s, e in tr_batches:
				reasoning_total_cost += model.batch_train_inference(train_q[s:e], train_p[s:e])

			tr_preds = model.predict(train_q, train_p, tr_batches_test)
			tr_pa, tr_al, tr_ast = multi_accuracy(train_p, tr_preds, multi_kb, FLAGS.steps, FLAGS.hops, FLAGS.lan_labels)
			v_preds = model.predict(valid_q, valid_p, v_batches)
			v_pa, v_al, v_ast = multi_accuracy(valid_p, v_preds, multi_kb, FLAGS.steps, FLAGS.hops, FLAGS.lan_labels)
			t_preds = model.predict(test_q, test_p, t_batches)
			t_pa, t_al, t_ast = multi_accuracy(test_p, t_preds, multi_kb, FLAGS.steps, FLAGS.hops, FLAGS.lan_labels)

			if v_ast > best_v_ast:
				best_v_ep = t
				best_v_ast = v_ast
				best_v_pa = v_pa
				best_v_al = v_al
				best_t_ast = t_ast
				best_t_pa = t_pa
				best_t_al = t_al
				model.store()

			print('--------------------------------------------------------------------------------------------'
			      '--------------------------------------------------------------------------------------------')
			print('Epoch', t)
			print('Timing', (time.time() - start))
			print('Embedding total cost for KG1:', kg1_embedding_cost)
			print('Embedding total cost for KG2:', kg2_embedding_cost)
			print('Reasoning total cost:', reasoning_total_cost)
			print('Training Accuracy:', t_ast, tr_pa, tr_al)
			print('Validation Accuracy:', v_ast, v_pa, v_al)
			print('Test Accuracy:', t_ast, t_pa, t_al)
			print('Best Validation epoch & accuracy & path accu & alignment accu:', best_v_ep, best_v_ast, best_v_pa, best_v_al)
			print('Test accuracy under best Validation epoch:', best_t_ast, best_t_pa, best_t_al)
			print('--------------------------------------------------------------------------------------------'
			      '--------------------------------------------------------------------------------------------')


if __name__ == '__main__':
	tf.app.run(main)
