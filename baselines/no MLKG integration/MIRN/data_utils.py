# coding: utf-8
"""Process input data.

Knowledge Base: h@@@r@@@t

Training/Testing data: question@@@answer@@@e1(l1)#r1(l1)#e2(l1)#e2(l2)#r2(l2)#e3(l2)
Note that the last item of each line should be an entity.
"""
from __future__ import absolute_import

import os
import numpy as np
import jieba


def read_knowledge_base_file(knowledge_base_file, separator="@@@"):
	"""
Reads a knowledge base file and saves all the entities and relations
to the passed parameters.
Example in knowledge_base_file: batch_kb1.txt h@@@r@@@t
"""
	rel2id = {'<end>': 0}
	ent2id = {'<unk>': 0}
	print("Reading knowledge base file...")
	if os.path.isfile(knowledge_base_file):
		with open(knowledge_base_file, encoding="utf-8") as f:
			lines = f.readlines()
	else:
		raise Exception("!! %s is not found!!" % knowledge_base_file)

	for line in lines:
		line = line.strip().split(separator)
		if line[0] not in ent2id.keys():
			ent2id[line[0]] = len(ent2id)
		if line[2] not in ent2id.keys():
			ent2id[line[2]] = len(ent2id)
		if line[1] not in rel2id.keys():
			rel2id[line[1]] = len(rel2id)
	return ent2id, rel2id


def get_knowledge_base(knowledge_base_file, ent2id, rel2id, separator="@@@"):
	"""
Create the KB Matrix whose elements are integers representing the knowledge base.
    :param separator: used to split a line of data
:param knowledge_base_file: Knowledge base file whose triples are separated by path_sep.
:param ent2id: Entity to ID dictionary.
:param rel2id: Relation to ID dictionary.
:return: Triples Numpy Array, KB Matrix whose maximum column index is the maximum number of tails for a single
head entity and relation pair, maximum tail number.
"""
	n_entities = len(ent2id)
	n_relations = len(rel2id)
	# tails = np.zeros([n_entities * n_relations, 1], 'int32')
	triples = []

	with open(knowledge_base_file, encoding="utf-8") as f:
		for line in f.readlines():
			line = line.strip().split(separator)

			h = ent2id[line[0]]
			r = rel2id[line[1]]
			t = ent2id[line[2]]
			triples.append([h, r, t])  # [h,r]->[h*n_relations+r]
			# tails[h * n_relations + r] += 1

	return np.array(triples) #, np.max(tails)


def read_dataset(data_file: str, data_sep = "\t"):
	if os.path.isfile(data_file):
		with open(data_file, encoding="utf-8") as f:
			lines = f.readlines()
	else:
		raise Exception("!! %s is not found!!" % data_file)
	labels = data_file.split(".")[0].strip("data/").split("_")
	lan_que = labels[0].lower()
	hops = (len(labels) - 1) if labels[-1] in {"zh", "en", "fr"} else (len(labels) - 2)
	print("Detected {} hop reasoning.".format(str(hops)))
	lan_labels = labels[1:hops+1]
	lan_labels.append(lan_labels[-1])
	# len(steps) == len(lan_labels) + 1, because the last reasoning is a dummy one
	steps = [0, 2]
	for i in range(hops - 1):
		if lan_labels[i + 1] == lan_labels[i]:
			steps.append(steps[i+1] + 2)
		else:
			steps.append(steps[i+1] + 3)
	is_cn = True if lan_que == "zh" else False
	if is_cn:
		print("Detected ZH question. Doing Chinese word segmentation.")
		jieba.load_userdict("data/zh_entities.txt")
	data = []  # question answer path
	questions = []
	qw2id = {'<unk>': 0}
	for line in lines:
		line = line.strip().split(data_sep)
		if is_cn:
			line[0] = " ".join(jieba.cut(line[0], cut_all=False))  # Use jieba to do word segmentation
		q_words_list = line[0].strip().split()
		data.append([line[0], line[1]])
		for w in q_words_list:
			if w not in qw2id.keys():
				qw2id[w] = len(qw2id)
		questions.append(q_words_list)

	sentence_size = max(len(i) for i in questions)

	return data, sentence_size, qw2id, hops, lan_que, lan_labels, steps


class KnowledgeBase(object):

	def __init__(self, knowledge_base_file, separator="@@@", name="kb"):
		self.name = name

		print("Processing knowledge base for " + name + "...")
		ent2id, rel2id = read_knowledge_base_file(knowledge_base_file, separator)
		self.entities = ent2id.keys()
		self.relations = rel2id.keys()
		self.rel2id = rel2id
		self.id2rel = {value:key for key, value in self.rel2id.items()}
		self.ent2id = ent2id
		self.id2ent = {value:key for key, value in self.ent2id.items()}
		self.id2ent[-1] = '<unk>'
		self.n_entities = len(self.ent2id)
		self.n_relations = len(self.rel2id)

		print('here are %d relations in rel2id(relation_vocabulary)' % self.n_relations)
		print('here are %d entities in ent2id(entity_vocabulary)' % self.n_entities)

		# self.triples, self.tails_size = get_knowledge_base(knowledge_base_file, self.ent2id, self.rel2id)

		self.triples = get_knowledge_base(knowledge_base_file, self.ent2id, self.rel2id)

		print("#number of Triples", len(self.triples))


class MultiKnowledgeBase(object):

	def __init__(self, kb1:KnowledgeBase, kb2:KnowledgeBase, align_correct, is_flip:False, separator="&&&"):
		self.a_array_correct = []
		self.kb1 = kb1
		self.kb2 = kb2
		self.align_dict_1_2 = {}
		self.align_dict_2_1 = {}
		self.name = self.kb1.name + "+" + self.kb2.name
		with open(align_correct, "r", encoding="utf-8") as ac:
			for line in ac.readlines():
				line = line.strip().split(separator)
				e1 = None
				e2 = None
				l0 = line[0] if not is_flip else line[1]
				l1 = line[1] if not is_flip else line[0]
				if l0 in self.kb1.ent2id.keys():
					e1 = self.kb1.ent2id[l0]
				if l1 in self.kb2.ent2id.keys():
					e2 = self.kb2.ent2id[l1]
				if e1 is not None and e2 is not None:
					self.align_dict_1_2[e1] = e2
					self.align_dict_2_1[e2] = e1
					self.a_array_correct.append((e1, e2))
		self.a_array_correct = np.array(self.a_array_correct)

		print("Loaded correct alignment pairs used for training) from", align_correct,
		      ". #pairs:", len(self.a_array_correct))

	def load_pred(self, align_pred_1_2, align_pred_2_1, sep_1="&&&", sep_2="\t", sep_3 = "@@@"):
		self.a_array_pred_1_2 = []
		self.a_array_pred_2_1 = []
		self.score_dict_1_2 = {}
		self.score_dict_2_1 = {}
		with open(align_pred_1_2, "r", encoding="utf-8") as ap12:
			for line in ap12.readlines():
				line = line.strip().split(sep_1)
				e1 = self.kb1.ent2id[line[0]]
				e1_dups = []
				preds_top_k_str = line[1].strip().split(sep_2)
				preds_top_k = []
				for p in preds_top_k_str:
					p = p.split(sep_3)
					e2 = self.kb2.ent2id[p[0]]
					scr = float(p[1])
					preds_top_k.append(e2)
					e1_dups.append(e1)
					self.score_dict_1_2[(e1, e2)] = scr
				self.a_array_pred_1_2.append((e1_dups, preds_top_k))

		with open(align_pred_2_1, "r", encoding="utf-8") as ap21:
			for line in ap21.readlines():
				line = line.strip().split(sep_1)
				e2 = self.kb2.ent2id[line[0]]
				e2_dups = []
				preds_top_k_str = line[1].strip().split(sep_2)
				preds_top_k = []
				for p in preds_top_k_str:
					p = p.split(sep_3)
					e1 = self.kb1.ent2id[p[0]]
					scr = float(p[1])
					preds_top_k.append(e1)
					e2_dups.append(e2)
					self.score_dict_2_1[(e2, e1)] = scr
				self.a_array_pred_2_1.append((e2_dups, preds_top_k))


		for i in range(len(self.kb1.ent2id)):
			self.score_dict_1_2[(i, -1)] = 0

		for j in range(len(self.kb2.ent2id)):
			self.score_dict_2_1[(j, -1)] = 0

		self.a_array_pred_1_2 = np.array(self.a_array_pred_1_2)
		self.a_array_pred_2_1 = np.array(self.a_array_pred_2_1)
		self.pred_k = self.a_array_pred_1_2.shape[2]
		print("Loaded alignment prediction pairs 1 to 2 from trained alignment model from", align_pred_1_2,
		      ". #pairs:", len(self.a_array_pred_1_2))
		print("Loaded alignment prediction pairs 2 to 1 from trained alignment model from", align_pred_2_1,
		      ". #pairs:", len(self.a_array_pred_2_1))
		print("Prediction is for top {}.".format(self.pred_k))


def process_dataset(data_file, multi_kb: MultiKnowledgeBase, data_sep="\t", path_sep="###", triple_sep="@@@"):
	data, sentence_size, qw2id, hops, lan_que, lan_labels, steps = read_dataset(data_file, data_sep)
	print('here are %d words in word2id(question vocab)' % len(qw2id))
	kb2_ent2id = multi_kb.kb2.ent2id
	kb1_ent2id = multi_kb.kb1.ent2id
	kb1_rel2id = multi_kb.kb1.rel2id
	kb2_rel2id = multi_kb.kb2.rel2id
	questions_ids = []
	questions_strings = []
	paths_ids = []
	paths_strings = []
	for q_str, p_str in data:
		q_strings = q_str.strip().split()
		questions_ids.append([qw2id[w] for w in q_strings] + [0] * max(0, sentence_size - len(q_strings)))
		questions_strings.append(q_strings)
		# answer id one-hot
		p_trps = p_str.strip().split(path_sep)
		paths_strings.append(p_trps)
		tps = []
		for triple in p_trps:
			tps.append(triple.split(triple_sep))
		p_ids = [kb1_ent2id[tps[0][0]], kb1_rel2id[tps[0][1]], kb1_ent2id[tps[0][2]]]
		for i in range(hops - 1):
			cur_tp = tps[i + 1]
			if lan_labels[i + 1] == lan_labels[i]:
				if lan_labels[i + 1] == lan_labels[0]:
					p_ids.extend([kb1_rel2id[cur_tp[1]], kb1_ent2id[cur_tp[2]]])
				else:
					p_ids.extend([kb2_rel2id[cur_tp[1]], kb2_ent2id[cur_tp[2]]])
			else:
				if lan_labels[i + 1] == lan_labels[0]:
					p_ids.extend([kb1_ent2id[cur_tp[0]], kb1_rel2id[cur_tp[1]], kb1_ent2id[cur_tp[2]]])
				else:
					p_ids.extend([kb2_ent2id[cur_tp[0]], kb2_rel2id[cur_tp[1]], kb2_ent2id[cur_tp[2]]])
		# to prevent exceeding array indices in the reasoning module (because tf.cond doesn't use short-circuit code.)
		p_ids.append(0)
		paths_ids.append(p_ids)
	return np.array(questions_ids), np.array(paths_ids), questions_strings, paths_strings, qw2id, sentence_size,\
	       len(qw2id), hops, lan_que, lan_labels, steps

def recover_predictions(output_file, predictions: np.ndarray, multi_kb: MultiKnowledgeBase, hops, lan_labels, steps,
                        separator="@@@"):
	out_strs = []
	kb2_id2ent = multi_kb.kb2.id2ent
	kb1_id2ent = multi_kb.kb1.id2ent
	kb1_id2rel = multi_kb.kb1.id2rel
	kb2_id2rel = multi_kb.kb2.id2rel
	for ist in predictions:
		str = kb1_id2ent[ist[0]]+separator+kb1_id2rel[ist[1]]+separator+kb1_id2ent[ist[2]]+separator
		for i in range(hops - 1):
			if lan_labels[i + 1] == lan_labels[i]:
				if lan_labels[i + 1] == lan_labels[0]:
					str+=kb1_id2rel[ist[steps[i + 1] + 1]]+separator+kb1_id2ent[ist[steps[i + 1] + 2]]+separator
				else:
					str+=kb2_id2rel[ist[steps[i + 1] + 1]]+separator+kb2_id2ent[ist[steps[i + 1] + 2]]+separator
			else:
				if lan_labels[i + 1] == lan_labels[0]:
					str+=kb1_id2ent[ist[steps[i + 1] + 1]]+separator+kb1_id2rel[ist[steps[i + 1] + 2]]+separator+\
					              kb1_id2ent[ist[steps[i + 1] + 3]]+separator
				else:
					str+=kb2_id2ent[ist[steps[i + 1] + 1]]+separator+kb2_id2rel[ist[steps[i + 1] + 2]]+separator+\
					              kb2_id2ent[ist[steps[i + 1] + 3]]+separator
		str = str.strip(separator) + "\n"
		out_strs.append(str)
	with open(output_file, "w", encoding="utf-8") as of:
		of.writelines(out_strs)
