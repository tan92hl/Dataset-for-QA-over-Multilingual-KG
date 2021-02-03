# coding=utf-8
from __future__ import print_function
import os
from platform import system

import numpy as np
import tensorflow as tf
from data_utils import MultiKnowledgeBase
from utils import add_gradient_noise, zero_nil_slot, orthogonal_initializer


class M_IRN(object):
    def __init__(self, config, multi_kb: MultiKnowledgeBase, sess):
        self._margin = 4
        self._dataset = config.dataset
        self._batch_size = config.batch_size
        self._sentence_size = config.sentence_size
        self._embedding_size = config.embedding_dimension
        self._max_grad_norm = config.max_grad_norm
        self._multi_kb = multi_kb
        self._vocab_size = config.question_words
        self._is_direct_align = config.direct_align
        self._is_dual_matrices = config.dual_matrices
        self._hops = config.hops
        self._steps = config.steps
        self._lan_labels = config.lan_labels
        self._lan_que = config.lan_que
        self._rel_size_1 = self._multi_kb.kb1.n_relations
        self._rel_size_2 = self._multi_kb.kb2.n_relations
        self._ent_size_1 = self._multi_kb.kb1.n_entities
        self._ent_size_2 = self._multi_kb.kb2.n_entities
        self._init = tf.contrib.layers.xavier_initializer()
        self._orthogonal_init = orthogonal_initializer()
        self._opt = tf.train.AdamOptimizer(learning_rate=config.lr, epsilon=config.epsilon, name="opt")
        # self._AM_opt = tf.train.AdamOptimizer(learning_rate=config.lr * config.ar, epsilon=config.epsilon,
        #                                       name="AM_opt")
        self._name = "M_IRN"
        self._checkpoint_dir = config.checkpoint_dir + '/' + config.kb_dir + '/' +self._name
        if not self._is_direct_align:
            self.this_k_1_2 = config.this_k_1_2
            self.this_k_2_1 = config.this_k_2_1

        if not os.path.exists(self._checkpoint_dir):
            os.makedirs(self._checkpoint_dir)

        self._build_inputs()
        self._build_vars()
        self._saver = tf.train.Saver(max_to_keep=1)

        # kg1 train and loss
        kg1_batch_loss = self._kg1_to_train()
        kg1_loss_op = tf.reduce_sum(kg1_batch_loss, name="KG1_loss_op")
        kg1_grads_and_vars = self._opt.compute_gradients(kg1_loss_op,
                                                         [self._kg1_ent_emb, self._kg1_rel_emb,
                                                          self._kg1_Mse])
        kg1_nil_grads_and_vars = []
        for g, v in kg1_grads_and_vars:
            if v.name in self._nil_vars:  # not _kg1_Mse
                kg1_nil_grads_and_vars.append((zero_nil_slot(g), v))
            else:
                kg1_nil_grads_and_vars.append((g, v))
        print("Gradients and Variables for KG1:")
        for g, v in kg1_nil_grads_and_vars:
            print(g, v.name)
        kg1_train_op = self._opt.apply_gradients(kg1_grads_and_vars, name="kg1_train_op")

        # kg2 train and loss
        kg2_batch_loss = self._kg2_to_train()
        kg2_loss_op = tf.reduce_sum(kg2_batch_loss, name="kg2_loss_op")
        kg2_grads_and_vars = self._opt.compute_gradients(kg2_loss_op,
                                                         [self._kg2_ent_emb, self._kg2_rel_emb,
                                                          self._kg2_Mse])
        kg2_nil_grads_and_vars = []
        for g, v in kg2_grads_and_vars:
            if v.name in self._nil_vars:  # not _kg2_Mse
                kg2_nil_grads_and_vars.append((zero_nil_slot(g), v))
            else:
                kg2_nil_grads_and_vars.append((g, v))
        print("Gradients and Variables for KG2:")
        for g, v in kg2_nil_grads_and_vars:
            print(g, v.name)
        kg2_train_op = self._opt.apply_gradients(kg2_grads_and_vars, name="kg2_train_op")

        # # alignment train and loss
        # alignment_batch_loss = self._align_to_train()
        # alignment_loss_op = tf.reduce_sum(alignment_batch_loss, name="alignment_loss_op")
        # alignment_train_op = self._AM_opt.minimize(alignment_loss_op)
        # ali_res_1_op, ali_res_2_op = self._align_kNN()

        # cross entropy as loss for inference:
        batch_loss, inference_path = self._inference()  # (batch_size, 1), (batch_size, 6)
        inference_loss_op = tf.reduce_sum(batch_loss, name="inference_loss_op")
        inference_params = [self._que_emb, self._kg1_Mrq, self._kg1_Mrs, self._kg2_Mrq, self._kg2_Mrs]
        inference_grads_and_vars = self._opt.compute_gradients(inference_loss_op, inference_params)
        inference_grads_and_vars = [(tf.clip_by_norm(g, self._max_grad_norm), v) for g, v in inference_grads_and_vars if
                                    g is not None]
        inference_grads_and_vars = [(add_gradient_noise(g), v) for g, v in inference_grads_and_vars]
        inference_nil_grads_and_vars = []
        for g, v in inference_grads_and_vars:
            if v.name in self._nil_vars:
                inference_nil_grads_and_vars.append((zero_nil_slot(g), v))
            else:
                inference_nil_grads_and_vars.append((g, v))
        print("Gradients and variables for inference:")
        for g, v in inference_nil_grads_and_vars:
            print(g, v.name)

        inference_train_op = self._opt.apply_gradients(inference_nil_grads_and_vars, name="inference_train_op")

        # batch_predict ops
        inference_predict_op = inference_path

        # assign ops
        self.kg1_loss_op = kg1_loss_op
        self.kg1_train_op = kg1_train_op
        self.kg2_loss_op = kg2_loss_op
        self.kg2_train_op = kg2_train_op
        # self.alignment_loss_op = alignment_loss_op
        # self.alignment_train_op = alignment_train_op
        self.inference_loss_op = inference_loss_op
        self.inference_predict_op = inference_predict_op
        self.inference_train_op = inference_train_op
        # self.ali_res_1 = ali_res_1_op
        # self.ali_res_2 = ali_res_2_op

        init_op = tf.global_variables_initializer()
        table_op = tf.tables_initializer()
        self._sess = sess
        self._sess.run(init_op)
        self._sess.run(table_op)

    def _build_inputs(self):
        self._kbs_1 = tf.placeholder(tf.int32, [None, 3], name="KBs_1")
        self._kbs_2 = tf.placeholder(tf.int32, [None, 3], name="KBs_2")
        self._alignments = tf.placeholder(tf.int32, [None, 2], name="alignment_seeds")
        self._queries = tf.placeholder(tf.int32, [None, self._sentence_size], name="queries")
        self._paths = tf.placeholder(tf.int32, [None, self._steps[-1] + 2], name="paths")
        self._padding_1 = tf.placeholder(tf.int32, [None], name="padding_1")  # for id_padding
        self._padding_2 = tf.placeholder(tf.int32, [None], name="padding_2")
        self._zeros = tf.placeholder(tf.float32, [None], name="zeros")
        self._isTrain = tf.placeholder(tf.int32, name="ground_truth")

    def _build_vars(self):
        with tf.variable_scope(self._name):
            # nil words are initialized with zero
            nil_word_slot = tf.zeros([1, self._embedding_size])
            nil_ent_rel_slot = tf.zeros([1, self._embedding_size])
            # build embeddings
            kg1_entity_slot = tf.concat(axis=0, values=[nil_ent_rel_slot, self._init([self._ent_size_1 - 1,
                                                                                      self._embedding_size])])
            kg2_entity_slot = tf.concat(axis=0, values=[nil_ent_rel_slot, self._init([self._ent_size_2 - 1,
                                                                                      self._embedding_size])])
            kg1_relation_slot = tf.concat(axis=0, values=[nil_ent_rel_slot, self._init([self._rel_size_1 - 1,
                                                                                        self._embedding_size])])
            kg2_relation_slot = tf.concat(axis=0, values=[nil_ent_rel_slot, self._init([self._rel_size_2 - 1,
                                                                                        self._embedding_size])])
            question_slot = tf.concat(axis=0, values=[nil_word_slot, self._init([self._vocab_size - 1,
                                                                                 self._embedding_size])])
            # encode entity to vector to calculate weight (Entity Embedding), and do l2 normalization
            self._kg1_ent_emb = tf.Variable(kg1_entity_slot, name="_kg1_ent_emb")
            self._kg1_e_norm = tf.nn.l2_normalize(self._kg1_ent_emb)
            self._kg2_ent_emb = tf.Variable(kg2_entity_slot, name="_kg2_ent_emb")
            self._kg2_e_norm = tf.nn.l2_normalize(self._kg2_ent_emb)
            # encode relation to vector (Relation Embedding), and do l2 normalization
            self._kg1_rel_emb = tf.Variable(kg1_relation_slot, name="_kg1_rel_emb")
            self._kg1_r_norm = tf.nn.l2_normalize(self._kg1_rel_emb)
            self._kg2_rel_emb = tf.Variable(kg2_relation_slot, name="_kg2_rel_emb")
            self._kg2_r_norm = tf.nn.l2_normalize(self._kg2_rel_emb)
            # encode question-words to vector (Question Embedding), and do l2 normalization
            self._que_emb = tf.Variable(question_slot, name="_que_emb")
            self._q_norm = tf.nn.l2_normalize(self._que_emb)
            # Transfer matrices, essentially the inference parameters
            self._kg1_Mrq = tf.Variable(self._init([self._embedding_size, self._embedding_size]), name="_kg1_Mrq")
            self._kg1_Mrs = tf.Variable(self._init([self._embedding_size, self._embedding_size]), name="_kg1_Mrs")
            self._kg1_Mse = tf.Variable(self._init([self._embedding_size, self._embedding_size]), name="_kg1_Mse")

            self._kg2_Mrq = tf.Variable(self._init([self._embedding_size, self._embedding_size]), name="_kg2_Mrq")
            self._kg2_Mrs = tf.Variable(self._init([self._embedding_size, self._embedding_size]), name="_kg2_Mrs")
            self._kg2_Mse = tf.Variable(self._init([self._embedding_size, self._embedding_size]), name="_kg2_Mse")
            # # Transfer matrix between two languages
            # self._e_M12 = tf.Variable(self._orthogonal_init([self._embedding_size, self._embedding_size]),
            #                           name="_e_M12")
            # self._e_M21 = tf.Variable(self._orthogonal_init([self._embedding_size, self._embedding_size]),
            #                           name="_e_M21")
            cor_align_array = self._multi_kb.a_array_correct
            cor_key_tsr = tf.constant(cor_align_array[:, 0])
            cor_val_tsr = tf.constant(cor_align_array[:, 1])
            self._cor_a_table_12 = tf.lookup.StaticHashTable(
                tf.lookup.KeyValueTensorInitializer(cor_key_tsr, cor_val_tsr), -1)
            self._cor_a_table_21 = tf.lookup.StaticHashTable(
                tf.lookup.KeyValueTensorInitializer(cor_val_tsr, cor_key_tsr), -1)
            if not self._is_direct_align:
                self._set_pred_table_2_1(self.this_k_2_1)
                self._set_pred_table_1_2(self.this_k_1_2)

        self._nil_vars = {self._kg1_ent_emb.name, self._kg2_ent_emb.name,
                          self._que_emb.name, self._kg2_rel_emb.name,
                          self._kg1_rel_emb.name}  # need to keep first line 0

    def _set_pred_table_1_2(self, k_idx):
        with tf.variable_scope(self._name):
            pred_align_array_1_2 = self._multi_kb.a_array_pred_1_2
            pred_key_tsr_1_2 = tf.constant(pred_align_array_1_2[:, 0, 0])
            pred_val_tsr_1_2 = tf.constant(pred_align_array_1_2[:, 1, k_idx])
            self._pred_a_table_12 = tf.lookup.StaticHashTable(
                tf.lookup.KeyValueTensorInitializer(pred_key_tsr_1_2, pred_val_tsr_1_2), -1)

    def _set_pred_table_2_1(self, k_idx):
        with tf.variable_scope(self._name):
            pred_align_array_2_1 = self._multi_kb.a_array_pred_2_1
            pred_key_tsr_2_1 = tf.constant(pred_align_array_2_1[:, 0, 0])
            pred_val_tsr_2_1 = tf.constant(pred_align_array_2_1[:, 1, k_idx])
            self._pred_a_table_21 = tf.lookup.StaticHashTable(
                tf.lookup.KeyValueTensorInitializer(pred_key_tsr_2_1, pred_val_tsr_2_1), -1)

    def _kg1_to_train(self):
        """

        :return: loss for kg1 embedding
        """
        with tf.variable_scope(self._name):
            heads_1 = self._kbs_1[:, 0]  # (batch) head
            relations_1 = self._kbs_1[:, 1]  # (batch) relation
            tails_1 = self._kbs_1[:, 2]  # (batch) tail
            tt = self._padding_1
            kg1_h_matrix = tf.nn.embedding_lookup(self._kg1_ent_emb, heads_1)  # (batch,e)
            kb1_r_matrix = tf.nn.embedding_lookup(self._kg1_rel_emb, relations_1)
            kb1_t_matrix = tf.nn.embedding_lookup(self._kg1_ent_emb, tails_1)
            kg1_tt_matrix = tf.nn.embedding_lookup(self._kg1_ent_emb, tt)
            kg1_l_matrix = tf.matmul((kg1_h_matrix + kb1_r_matrix), self._kg1_Mse)  # M(h+r)
            kg1_loss_matrix = (kg1_l_matrix - kb1_t_matrix) * (kg1_l_matrix - kb1_t_matrix)
            kg1_neg_matrix = (kg1_l_matrix - kg1_tt_matrix) * (kg1_l_matrix - kg1_tt_matrix)
            kg1_emb_loss = self._margin + tf.reduce_sum(kg1_loss_matrix, 1) - tf.reduce_sum(kg1_neg_matrix, 1)
            kg1_emb_loss = tf.maximum(0.00, kg1_emb_loss)

            return kg1_emb_loss

    def _kg2_to_train(self):
        """

        :return: loss for kg2 embedding
        """
        with tf.variable_scope(self._name):
            heads_2 = self._kbs_2[:, 0]
            relations_2 = self._kbs_2[:, 1]
            tails_2 = self._kbs_2[:, 2]
            tt = self._padding_2
            kg2_h_matrix = tf.nn.embedding_lookup(self._kg2_ent_emb, heads_2)  # (batch,e)
            kg2_r_matrix = tf.nn.embedding_lookup(self._kg2_rel_emb, relations_2)
            kg2_t_matrix = tf.nn.embedding_lookup(self._kg2_ent_emb, tails_2)
            kg2_tt_matrix = tf.nn.embedding_lookup(self._kg2_ent_emb, tt)
            kg2_l_matrix = tf.matmul((kg2_h_matrix + kg2_r_matrix), self._kg2_Mse)  # M(h+r)
            kg2_loss_matrix = (kg2_l_matrix - kg2_t_matrix) * (kg2_l_matrix - kg2_t_matrix)
            kg2_neg_matrix = (kg2_l_matrix - kg2_tt_matrix) * (kg2_l_matrix - kg2_tt_matrix)
            kg2_emb_loss = self._margin + tf.reduce_sum(kg2_loss_matrix, 1) - tf.reduce_sum(kg2_neg_matrix, 1)
            kg2_emb_loss = tf.maximum(0.00, kg2_emb_loss)

            return kg2_emb_loss

    # def _align_to_train(self):
    #     with tf.variable_scope(self._name):
    #         kg1_entity_ids = self._alignments[:, 0]
    #         kg1_entity_emb = tf.nn.l2_normalize(tf.nn.embedding_lookup(self._kg1_ent_emb, kg1_entity_ids),1)
    #         kg2_entity_ids = self._alignments[:, 1]
    #         kg2_entity_emb = tf.nn.l2_normalize(tf.nn.embedding_lookup(self._kg2_ent_emb, kg2_entity_ids),1)
    #         alignment_loss_matrix = tf.subtract(tf.matmul(kg1_entity_emb, self._e_M12), kg2_entity_emb)
    #         alignment_loss = tf.reduce_sum(tf.sqrt(tf.reduce_sum(tf.square(alignment_loss_matrix), 1)))
    #         if self._is_dual_matrices:
    #             alignment_loss_matrix = tf.subtract(tf.matmul(kg2_entity_emb, self._e_M21), kg1_entity_emb)
    #             alignment_loss += tf.reduce_sum(tf.sqrt(tf.reduce_sum(tf.square(alignment_loss_matrix), 1)))
    #         return alignment_loss

    # def _align_kNN(self):
    #     with tf.variable_scope(self._name):
    #         kg1_entity_ids = self._alignments[:, 0]
    #         kg1_entity_emb = tf.nn.l2_normalize(tf.nn.embedding_lookup(self._kg1_ent_emb, kg1_entity_ids), 1)
    #         kg2_entity_ids = self._alignments[:, 1]
    #         kg2_entity_emb = tf.nn.l2_normalize(tf.nn.embedding_lookup(self._kg2_ent_emb, kg2_entity_ids), 1)
    #
    #         _, kg2_ent_preds = tf.nn.top_k(tf.matmul(tf.matmul(kg1_entity_emb, self._e_M12), self._kg2_ent_emb,
    #                                                  transpose_b=True), k=self._topK)
    #         _, kg1_ent_preds = tf.nn.top_k(tf.matmul(tf.matmul(kg2_entity_emb,
    #                                                            self._e_M21 if self._is_dual_matrices else
    #                                                            tf.matrix_inverse(self._e_M12)), self._kg1_ent_emb,
    #                                                  transpose_b=True), k=self._topK)
    #         return kg1_ent_preds, kg2_ent_preds

    def _inference(self):
        with tf.variable_scope(self._name):
            # Input module
            # Ax_ij shape is (batch_size, sentence_size ,embedding_size)
            query_word_emb = tf.nn.embedding_lookup(self._que_emb, self._queries)
            # Global question embedding. When the languages
            ques_emb = tf.reduce_sum(query_word_emb, 1)  # shape is (batch_size, embedding_size)
            loss = tf.reshape(self._zeros, [-1, 1], name='loss')  # (batch_size, 1)
            # The first state (entity) is given.
            init_state_index = tf.reshape(self._paths[:, 0], [-1, 1])  # (batch_size, 1)
            # KG1 is the first KG to be used in the path, KG2 the other.
            # Only in answer module do we cross language for state embedding.
            state_emb = tf.nn.embedding_lookup(self._kg1_ent_emb, init_state_index)  # (b,1)->(b,1,e)
            state_emb = tf.squeeze(state_emb, [1])  # (batch_size, embedding_size)
            dir_align = tf.constant(self._is_direct_align, dtype=tf.bool)
            # e_M21 = tf.matrix_inverse(self._e_M12)
            # Reasoning module
            path = pre_t_idx = init_state_index
            for hop in range(self._hops):
                step = self._steps[hop]
                py_is_1 = self._lan_labels[hop] == self._lan_labels[0]
                is_1 = tf.constant(py_is_1, dtype=tf.bool)
                py_is_cross = hop != 0 and (self._lan_labels[hop] != self._lan_labels[hop - 1])
                is_cross = tf.constant(py_is_cross, dtype=tf.bool)

                # Cross-lingual processing
                # head_emb = tf.cond(is_1,
                #                    lambda: tf.matmul(tf.nn.embedding_lookup(self._kg2_ent_emb,
                #                                                             tf.cast(pre_t_idx, tf.int64)),
                #                                      tf.cond(tf.constant(self._is_dual_matrices),
                #                                              lambda: self._e_M21,
                #                                              lambda: e_M21)),
                #                    lambda: tf.matmul(tf.nn.embedding_lookup(self._kg1_ent_emb,
                #                                                             tf.cast(pre_t_idx, tf.int64)), self._e_M12))
                # head_logits = tf.cond(is_1,
                #                       lambda: tf.matmul(head_emb, self._kg1_ent_emb, transpose_b=True),
                #                       lambda: tf.matmul(head_emb, self._kg2_ent_emb, transpose_b=True))
                if system() == "Windows":
                    # Windows compatible
                    if self._is_direct_align:
                        head_index = tf.cond(is_1, lambda: self._cor_a_table_21.lookup(tf.cast(pre_t_idx, tf.int32)),
                                             lambda: self._cor_a_table_12.lookup(tf.cast(pre_t_idx, tf.int32)))
                    else:
                        head_index = tf.cond(is_1, lambda: self._pred_a_table_21.lookup(tf.cast(pre_t_idx, tf.int32)),
                                             lambda: self._pred_a_table_12.lookup(tf.cast(pre_t_idx, tf.int32)))

                else:
                    # Linux compatible
                    if self._is_direct_align:
                        head_index = tf.cond(is_1, lambda: self._cor_a_table_21.lookup(tf.cast(pre_t_idx, tf.int64)),
                                             lambda: self._cor_a_table_12.lookup(tf.cast(pre_t_idx, tf.int64)))
                    else:
                        head_index = tf.cond(is_1, lambda: self._pred_a_table_21.lookup(tf.cast(pre_t_idx, tf.int64)),
                                             lambda: self._pred_a_table_12.lookup(tf.cast(pre_t_idx, tf.int64)))

                path = tf.cond(is_cross,
                               lambda: tf.concat(axis=1, values=[path, tf.reshape(tf.cast(head_index, tf.int32),
                                                                                  [-1, 1])]),
                               lambda: path)

                state_emb = tf.cond(is_cross,
                                    lambda: tf.cond(is_1, lambda: tf.nn.embedding_lookup(self._kg1_ent_emb, head_index),
                                                    lambda: tf.nn.embedding_lookup(self._kg2_ent_emb, head_index)),
                                    lambda: state_emb)

                gate = tf.matmul(ques_emb,
                                 tf.cond(is_1,
                                         lambda: tf.matmul(self._kg1_rel_emb, self._kg1_Mrq),
                                         lambda: tf.matmul(self._kg2_rel_emb, self._kg2_Mrq)), transpose_b=True) \
                       + tf.matmul(state_emb,
                                   tf.cond(is_1,
                                           lambda: tf.matmul(self._kg1_rel_emb, self._kg1_Mrs),
                                           lambda: tf.matmul(self._kg2_rel_emb, self._kg2_Mrs)), transpose_b=True)
                relation_logits = gate
                relation_index = tf.argmax(relation_logits, 1)
                gate = tf.nn.softmax(gate)
                real_rel_one_hot = tf.cond(is_cross,
                                           lambda: tf.one_hot(self._paths[:, step + 2],
                                                              tf.cond(is_1, lambda: tf.constant(self._rel_size_1),
                                                                      lambda: tf.constant(self._rel_size_2)),
                                                              on_value=1.0, off_value=0.0, axis=-1),
                                           lambda: tf.one_hot(self._paths[:, step + 1],
                                                              tf.cond(is_1, lambda: tf.constant(self._rel_size_1),
                                                                      lambda: tf.constant(self._rel_size_2)),
                                                              on_value=1.0, off_value=0.0, axis=-1))
                state_emb = state_emb + tf.matmul(gate,
                                                  tf.cond(is_1,
                                                          lambda: tf.matmul(self._kg1_rel_emb, self._kg1_Mrs),
                                                          lambda: tf.matmul(self._kg2_rel_emb, self._kg2_Mrs)))
                loss += tf.reshape(tf.nn.softmax_cross_entropy_with_logits(logits=relation_logits,
                                                                           labels=real_rel_one_hot), [-1, 1])  # (b,1)
                ques_emb = ques_emb - tf.matmul(gate, tf.cond(is_1,
                                                              lambda: tf.matmul(self._kg1_rel_emb, self._kg1_Mrq),
                                                              lambda: tf.matmul(self._kg2_rel_emb, self._kg2_Mrq)))

                # Answer module
                tail_logits = tf.cond(is_1,
                                      lambda: tf.matmul(tf.matmul(state_emb, self._kg1_Mse),
                                                        self._kg1_ent_emb, transpose_b=True),
                                      lambda: tf.matmul(tf.matmul(state_emb, self._kg2_Mse),
                                                        self._kg2_ent_emb, transpose_b=True))
                tail_index = tf.argmax(tail_logits, 1)
                # # (batch_size, embedding_size)
                # tail_index = tf.cast(tail_index, tf.float32)
                # relation_index = tf.cast(relation_index, tf.float32)
                # # if relation_index == 0, stop inference, tail_index = previous tail; if not, tail won't change
                # tail_index = relation_index / (relation_index + 1e-15) * tail_index \
                #              + (1 - relation_index / (relation_index + 1e-15)) * tf.cast(path[:, -1], tf.float32)
                path = tf.concat(axis=1, values=[path, tf.reshape(tf.cast(relation_index, tf.int32), [-1, 1])])
                path = tf.concat(axis=1, values=[path, tf.reshape(tf.cast(tail_index, tf.int32), [-1, 1])])
                # (b,self._rel_size_1)
                real_tail_one_hot = tf.cond(is_cross,
                                            lambda: tf.one_hot(self._paths[:, step + 3],
                                                               tf.cond(is_1, lambda: tf.constant(self._ent_size_1),
                                                                       lambda: tf.constant(self._ent_size_2)),
                                                               on_value=1.0, off_value=0.0, axis=-1),
                                            lambda: tf.one_hot(self._paths[:, step + 2],
                                                               tf.cond(is_1, lambda: tf.constant(self._ent_size_1),
                                                                       lambda: tf.constant(self._ent_size_2)),
                                                               on_value=1.0, off_value=0.0, axis=-1))
                loss += tf.reshape(tf.nn.softmax_cross_entropy_with_logits(logits=tail_logits,
                                                                           labels=real_tail_one_hot), [-1, 1])  # (b,1)

                pre_t_idx = tail_index
            return loss, path

    def batch_train_kg1_embedding(self, batch_kb1):
        """
        Args:
            batch_kb1: Tensor (None, memory_size_1, 3)

        Returns:
            loss: floating-point number, the loss computed for the batch
        """
        kg1_n_example = batch_kb1.shape[0]
        pad_1 = np.random.randint(low=0, high=self._ent_size_1, size=kg1_n_example)

        feed_dict = {self._kbs_1: batch_kb1, self._padding_1: pad_1, self._isTrain: 0}

        kg1_loss, _1 = self._sess.run([self.kg1_loss_op, self.kg1_train_op], feed_dict=feed_dict)
        # self._kg1_ent_emb = tf.nn.l2_normalize(self._kg1_ent_emb,1)
        # self._kg1_rel_emb = tf.nn.l2_normalize(self._kg1_rel_emb,1)
        return kg1_loss

    def batch_train_kg2_embedding(self, batch_kb2):
        """
        Args:
            batch_kb2: Tensor (None, memory_size_1, 3)

        Returns:
            loss: floating-point number, the loss computed for the batch
        """
        kg2_n_example = batch_kb2.shape[0]
        pad_2 = np.random.randint(low=0, high=self._ent_size_2, size=kg2_n_example)

        feed_dict = {self._kbs_2: batch_kb2, self._padding_2: pad_2, self._isTrain: 0}

        kg2_loss, _2 = self._sess.run([self.kg2_loss_op, self.kg2_train_op], feed_dict=feed_dict)
        return kg2_loss

    # def batch_train_alignment(self, alignment_seeds):
    #     feed_dict = {self._alignments: alignment_seeds}
    #     loss, _ = self._sess.run([self.alignment_loss_op, self.alignment_train_op], feed_dict=feed_dict)
    #     return loss

    def batch_train_inference(self, queries, paths):
        """
        Args:
            queries: Tensor (None, sentence_size)
            paths: Tensor

        Returns:
            loss: floating-point number, the loss computed for the batch
        """
        n_example = queries.shape[0]
        zeros = np.zeros(n_example)
        feed_dict = {self._queries: queries, self._paths: paths, self._zeros: zeros, self._isTrain: 0}
        loss, _ = self._sess.run([self.inference_loss_op, self.inference_train_op], feed_dict=feed_dict)
        self._kg1_ent_emb = self._sess.run(self._kg1_e_norm)
        self._kg1_rel_emb = self._sess.run(self._kg1_r_norm)
        self._kg2_ent_emb = self._sess.run(self._kg2_e_norm)
        self._kg2_rel_emb = self._sess.run(self._kg2_r_norm)
        self._que_emb = self._sess.run(self._q_norm)
        return loss

    def batch_predict(self, queries, paths):
        """Predicts answers as one-hot encoding.

        Args:
            queries: Tensor (None, sentence_size)
            paths: Tensor(None, 6)

        Returns:
            answers: id (None, 1)  ,predict_op = max(1, [None,ent_size])
            :param queries:
            :param paths:
        """
        n_example = queries.shape[0]
        zeros = np.zeros(n_example)
        feed_dict = {self._queries: queries, self._paths: paths, self._zeros: zeros, self._isTrain: 1}
        return self._sess.run(self.inference_predict_op, feed_dict=feed_dict)

    def predict(self, quires, path, batches):
        res = []
        for s, e in batches:
            res.extend(self.batch_predict(quires[s:e], path[s:e]))
        return np.array(res)

    # def align_res(self, alignments, batches, topK):
    #     aligned_1 = []
    #     aligned_2 = []
    #     for s, e in batches:
    #         a1, a2 = self._sess.run([self.ali_res_1, self.ali_res_2], feed_dict={self._alignments: alignments[s:e],
    #                                                                              self._topK: topK})
    #         aligned_1.extend(a1)
    #         aligned_2.extend(a2)
    #
    #     hits20_12 = 0
    #     hits20_21 = 0
    #     for i in range(len(alignments)):
    #         if alignments[i, 1] in aligned_2[i]:
    #             hits20_12 += 1
    #         if alignments[i, 0] in aligned_1[i]:
    #             hits20_21 += 1
    #     hits20_12 = hits20_12/float(len(alignments))
    #     hits20_21 = hits20_21/float(len(alignments))
    #     return hits20_12, hits20_21

    def store(self):
        # attr = "direct_align" if self._is_direct_align else "MTransE"
        file = os.path.join(self._checkpoint_dir, self._name)
        print(" [*] save current parameters to %s." % file)
        self._saver.save(self._sess, file)

    def load(self):
        print(" [*] Reading checkpoints...")
        # attr = "direct_align" # if self._is_direct_align else "MTransE"
        checkpoint = tf.train.get_checkpoint_state(self._checkpoint_dir)
        if checkpoint and checkpoint.model_checkpoint_path:
            print("[*] Read from %s" % checkpoint.model_checkpoint_path)
            self._saver.restore(self._sess, checkpoint.model_checkpoint_path)
        else:
            print(" [!] Test mode but no checkpoint found")
