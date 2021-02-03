import os
import pickle
from collections import defaultdict
import itertools
import operator
from torch.utils.data import DataLoader, Dataset
import torch
import json
from functools import reduce
from itertools import accumulate
import random
from transformers import BertTokenizer as bt
from transformers import BertModel as bm
from transformers import BertConfig as bc

U_PATH, B_PATH = {}, {}
U_PATH['wq'] = '../data/WQ/main_exp'
U_PATH['wq_train1test2'] = '../data/WQ/train1test2_exp'
U_PATH['sq'] = '../data/SQ'
for i in [1,2,3]:
    U_PATH[f'pq{i}'] = f'../data/PQ/PQ{i}'
    U_PATH[f'pql{i}'] = f'../data/PQ/PQL{i}'
for i in range(11):
    U_PATH[f'wpq{i}'] = f'../data/PQ/exp3/UHop/{i}'
U_PATH['exp4'] = '../data/PQ/exp4'
U_PATH['grid2_4'] = '../data/grid-world/problem_16_4_2'
U_PATH['grid4_6'] = '../data/grid-world/problem_16_6_4'
U_PATH['grid6_8'] = '../data/grid-world/problem_16_8_6'
U_PATH['grid8_10'] = '../data/grid-world/problem_16_10_8'

U_PATH['mlpq-en-fr'] = '../data/MLPQ/en-fr/total/'
U_PATH['mlpq-en-fr_en-2h'] = '../data/MLPQ/en-fr/en/2-hop'
U_PATH['mlpq-en-fr_en-3h'] = '../data/MLPQ/en-fr/en/3-hop'
U_PATH['mlpq-en-fr_fr-2h'] = '../data/MLPQ/en-fr/fr/2-hop'
U_PATH['mlpq-en-fr_fr-3h'] = '../data/MLPQ/en-fr/fr/3-hop'
U_PATH['mlpq-en-fr_zh-2h'] = '../data/MLPQ/en-fr/zh/2-hop'
U_PATH['mlpq-en-fr_zh-3h'] = '../data/MLPQ/en-fr/zh/3-hop'
U_PATH['mlpq-en-fr_nmn'] = '../data/MLPQ/en-fr/total_NMN/'
U_PATH['mlpq-en-fr_nmn_en-2h'] = '../data/MLPQ/en-fr/en/2-hop_NMN'
U_PATH['mlpq-en-fr_nmn_en-3h'] = '../data/MLPQ/en-fr/en/3-hop_NMN'
U_PATH['mlpq-en-fr_nmn_fr-2h'] = '../data/MLPQ/en-fr/fr/2-hop_NMN'
U_PATH['mlpq-en-fr_nmn_fr-3h'] = '../data/MLPQ/en-fr/fr/3-hop_NMN'
U_PATH['mlpq-en-fr_nmn_zh-2h'] = '../data/MLPQ/en-fr/zh/2-hop_NMN'
U_PATH['mlpq-en-fr_nmn_zh-3h'] = '../data/MLPQ/en-fr/zh/3-hop_NMN'

U_PATH['mlpq-en-zh'] = '../data/MLPQ/en-zh/total/'
U_PATH['mlpq-en-zh_en-2h'] = '../data/MLPQ/en-zh/en/2-hop'
U_PATH['mlpq-en-zh_en-3h'] = '../data/MLPQ/en-zh/en/3-hop'
U_PATH['mlpq-en-zh_fr-2h'] = '../data/MLPQ/en-zh/fr/2-hop'
U_PATH['mlpq-en-zh_fr-3h'] = '../data/MLPQ/en-zh/fr/3-hop'
U_PATH['mlpq-en-zh_zh-2h'] = '../data/MLPQ/en-zh/zh/2-hop'
U_PATH['mlpq-en-zh_zh-3h'] = '../data/MLPQ/en-zh/zh/3-hop'
U_PATH['mlpq-en-zh_nmn'] = '../data/MLPQ/en-zh/total_NMN/'
U_PATH['mlpq-en-zh_nmn_en-2h'] = '../data/MLPQ/en-zh/en/2-hop_NMN'
U_PATH['mlpq-en-zh_nmn_en-3h'] = '../data/MLPQ/en-zh/en/3-hop_NMN'
U_PATH['mlpq-en-zh_nmn_fr-2h'] = '../data/MLPQ/en-zh/fr/2-hop_NMN'
U_PATH['mlpq-en-zh_nmn_fr-3h'] = '../data/MLPQ/en-zh/fr/3-hop_NMN'
U_PATH['mlpq-en-zh_nmn_zh-2h'] = '../data/MLPQ/en-zh/zh/2-hop_NMN'
U_PATH['mlpq-en-zh_nmn_zh-3h'] = '../data/MLPQ/en-zh/zh/3-hop_NMN'

U_PATH['mlpq-zh-fr'] = '../data/MLPQ/zh-fr/total/'
U_PATH['mlpq-zh-fr_en-2h'] = '../data/MLPQ/zh-fr/en/2-hop'
U_PATH['mlpq-zh-fr_en-3h'] = '../data/MLPQ/zh-fr/en/3-hop'
U_PATH['mlpq-zh-fr_fr-2h'] = '../data/MLPQ/zh-fr/fr/2-hop'
U_PATH['mlpq-zh-fr_fr-3h'] = '../data/MLPQ/zh-fr/fr/3-hop'
U_PATH['mlpq-zh-fr_zh-2h'] = '../data/MLPQ/zh-fr/zh/2-hop'
U_PATH['mlpq-zh-fr_zh-3h'] = '../data/MLPQ/zh-fr/zh/3-hop'
U_PATH['mlpq-zh-fr_nmn'] = '../data/MLPQ/zh-fr/total_NMN/'
U_PATH['mlpq-zh-fr_nmn_en-2h'] = '../data/MLPQ/zh-fr/en/2-hop_NMN'
U_PATH['mlpq-zh-fr_nmn_en-3h'] = '../data/MLPQ/zh-fr/en/3-hop_NMN'
U_PATH['mlpq-zh-fr_nmn_fr-2h'] = '../data/MLPQ/zh-fr/fr/2-hop_NMN'
U_PATH['mlpq-zh-fr_nmn_fr-3h'] = '../data/MLPQ/zh-fr/fr/3-hop_NMN'
U_PATH['mlpq-zh-fr_nmn_zh-2h'] = '../data/MLPQ/zh-fr/zh/2-hop_NMN'
U_PATH['mlpq-zh-fr_nmn_zh-3h'] = '../data/MLPQ/zh-fr/zh/3-hop_NMN'

ACC_COUNT = {}
ACC_COUNT['mlpq-en-fr'] = 14208
ACC_COUNT['mlpq-en-fr_en-2h'] = 998
ACC_COUNT['mlpq-en-fr_en-3h'] = 3738
ACC_COUNT['mlpq-en-fr_fr-2h'] = 998
ACC_COUNT['mlpq-en-fr_fr-3h'] = 3738
ACC_COUNT['mlpq-en-fr_zh-2h'] = 998
ACC_COUNT['mlpq-en-fr_zh-3h'] = 3738
ACC_COUNT['mlpq-en-fr_nmn'] = 14208
ACC_COUNT['mlpq-en-fr_nmn_en-2h'] = 998
ACC_COUNT['mlpq-en-fr_nmn_en-3h'] = 3738
ACC_COUNT['mlpq-en-fr_nmn_fr-2h'] = 998
ACC_COUNT['mlpq-en-fr_nmn_fr-3h'] = 3738
ACC_COUNT['mlpq-en-fr_nmn_zh-2h'] = 998
ACC_COUNT['mlpq-en-fr_nmn_zh-3h'] = 3738

ACC_COUNT['mlpq-en-zh'] = 9771
ACC_COUNT['mlpq-en-zh_en-2h'] = 1015
ACC_COUNT['mlpq-en-zh_en-3h'] = 2242
ACC_COUNT['mlpq-en-zh_fr-2h'] = 1015
ACC_COUNT['mlpq-en-zh_fr-3h'] = 2242
ACC_COUNT['mlpq-en-zh_zh-2h'] = 1015
ACC_COUNT['mlpq-en-zh_zh-3h'] = 2242
ACC_COUNT['mlpq-en-zh_nmn'] = 9771
ACC_COUNT['mlpq-en-zh_nmn_en-2h'] = 1015
ACC_COUNT['mlpq-en-zh_nmn_en-3h'] = 2242
ACC_COUNT['mlpq-en-zh_nmn_fr-2h'] = 1015
ACC_COUNT['mlpq-en-zh_nmn_fr-3h'] = 2242
ACC_COUNT['mlpq-en-zh_nmn_zh-2h'] = 1015
ACC_COUNT['mlpq-en-zh_nmn_zh-3h'] = 2242

ACC_COUNT['mlpq-zh-fr'] = 8724
ACC_COUNT['mlpq-zh-fr_en-2h'] = 561
ACC_COUNT['mlpq-zh-fr_en-3h'] = 2347
ACC_COUNT['mlpq-zh-fr_fr-2h'] = 561
ACC_COUNT['mlpq-zh-fr_fr-3h'] = 2347
ACC_COUNT['mlpq-zh-fr_zh-2h'] = 561
ACC_COUNT['mlpq-zh-fr_zh-3h'] = 2347
ACC_COUNT['mlpq-zh-fr_nmn'] = 8724
ACC_COUNT['mlpq-zh-fr_nmn_en-2h'] = 561
ACC_COUNT['mlpq-zh-fr_nmn_en-3h'] = 2347
ACC_COUNT['mlpq-zh-fr_nmn_fr-2h'] = 561
ACC_COUNT['mlpq-zh-fr_nmn_fr-3h'] = 2347
ACC_COUNT['mlpq-zh-fr_nmn_zh-2h'] = 561
ACC_COUNT['mlpq-zh-fr_nmn_zh-3h'] = 2347


B_PATH['wq'] = '../data/baseline/KBQA_RE_data/webqsp_relations/MODE_data.txt'
#PATH['wq'] = '../data/baseline/KBQA_RE_data/webqsp_relations/WebQSP.RE.MODE.with_boundary.withpool.dlnlp.txt'
B_PATH['sq'] = '../data/baseline/KBQA_RE_data/sq_relations/MODE.replace_ne.withpool'
for i in [1,2,3]:
    B_PATH[f'pq{i}'] = f'../data/PQ/baseline/PQ{i}/MODE_data1.txt'
    B_PATH[f'pql{i}'] = f'../data/PQ/baseline/PQL{i}/MODE_data1.txt'
for i in range(11):
    B_PATH[f'wpq{i}'] = f'../data/PQ/exp3/baseline/{i}/MODE_data.txt'
B_PATH['exp4'] = '../data/PQ/exp4/baseline/MODE_data.txt'

from itertools import accumulate

def quick_collate(batch):
    return batch[0]

def random_split(dataset, train_p, valid_p):
    random.shuffle(dataset.data_objs)
    return Subset(dataset.data_objs[:int(len(dataset)*train_p)]), Subset(dataset.data_objs[int(len(dataset)*train_p):])

def load_bert_from_tf(BERT_PT_PATH):
    bert_config_file = os.path.join(BERT_PT_PATH, f'config.json')

    bert_tokenizer = bt.from_pretrained(BERT_PT_PATH)
    bert_model = bm.from_pretrained(BERT_PT_PATH)
    bert_config = bc.from_pretrained(BERT_PT_PATH)
    return bert_model, bert_tokenizer, bert_config

class Subset(Dataset):
    def __init__(self, data_objs):
        self.data_objs = data_objs
    def __getitem__(self, idx):
        return self.data_objs[idx]
    def __len__(self):
        return len(self.data_objs)

class PerQuestionDataset(Dataset):
    def __init__(self, args, mode, word2id, rela2id, bert_tokenizer):
        super(PerQuestionDataset, self).__init__()
        self.bert_tokenizer = bert_tokenizer
        self.data_objs = self._get_data(args, mode, word2id, rela2id)

    def _get_data(self, args, mode, word2id, rela2id):
        data_objs = []
        if args.framework == 'UHop':
            file_path = U_PATH[args.dataset]
            print(file_path)
            with open(f'{file_path}/{mode}_data.txt', 'r') as f:
                for i, line in enumerate(f):
                    print(f'\rreading line {i}', end='')
                    data = json.loads(line)
                    data = self._numericalize(data, word2id, rela2id, args.q_representation, 'UHop')
                    data_objs.append(data)
        elif args.framework == 'baseline':
            file_path = B_PATH[args.dataset.lower()]
            print(file_path)
            with open(file_path.replace('MODE', mode), 'r') as f:
                for i, line in enumerate(f):
                    print(f'\rreading line {i}', end='')
                    anses, candidates, question = line.strip().split('\t')
                    # modify because of 'noNegativeAnswer' in sq data
                    candidates = [[x, [], 0] for x in candidates.split() if x not in anses.split() and x!='noNegativeAnswer']
                    # modify for "#head_entity#" label in sq dataset
                    ques = question.replace('$ARG1', '').replace('$ARG2', '')
                    ques = ques.replace('<e>', 'TOPIC_ENTITY').replace('#head_entity#', 'TOPIC_ENTITY').strip()
                    for ans in anses.split():
                        data = (i, ques, [[[ans, [], 1]]+candidates])
                        data = self._numericalize(data, word2id, rela2id, args.q_representation, 'baseline')
                        data_objs.append(data)
        return data_objs
    def _numericalize(self, data, word2id, rela2id, q_representation, framework):
        index, ques, step_list = data[0], data[1], data[2]
        if q_representation == "bert":
            ques = self._bert_numericalize_str(ques)
        else:
            ques = self._numericalize_str(ques, word2id, [' '])
        if framework == 'baseline':
            tuples = []
            for t in step_list[0]:
                num_rela = self._numericalize_str(t[0], rela2id, ['.'])
                num_rela_text = self._numericalize_str(t[0], word2id, ['.', '_'])
                num_prev = [self._numericalize_str(prev, rela2id, ['.']) for prev in t[1]]
                num_prev_text = [self._numericalize_str(prev, word2id, ['.', '_']) for prev in t[1]]
                tuples.append((num_rela, num_rela_text, num_prev, num_prev_text, t[2]))
            new_step_list = tuples
        else:
            new_step_list = []
            for step in step_list:
                new_step = []
                for t in step:
                    num_rela = self._numericalize_str(t[0], rela2id, ['.'])
                    num_rela_text = self._numericalize_str(t[0], word2id, ['.', '_'])
                    num_prev = [self._numericalize_str(prev, rela2id, ['.']) for prev in t[1]]
                    num_prev_text = [self._numericalize_str(prev, word2id, ['.', '_']) for prev in t[1]]
                    new_step.append((num_rela, num_rela_text, num_prev, num_prev_text, t[2]))
                new_step_list.append(new_step)
        return index, ques, new_step_list
    def _numericalize_str(self, string, map2id, dilemeter):
        #print('original str:', string)
        if len(dilemeter) == 2:
            string = string.replace(dilemeter[1], dilemeter[0])
        dilemeter = dilemeter[0]
        tokens = string.strip().split(dilemeter)
        tokens = [map2id[x] if x in map2id else map2id['<unk>'] for x in tokens]
        #print('tokens:', tokens)
        return tokens
    def _bert_numericalize_str(self, seq):
        tokens = self.bert_tokenizer.tokenize(seq)
        tokens = ['[CLS]'] + tokens + ['[SEP]']
        tokens = self.bert_tokenizer.convert_tokens_to_ids(tokens)
        return tokens
    def __len__(self):
        return len(self.data_objs)
    def __getitem__(self, index):
        return self.data_objs[index]


class PerQuestionDatasetMLPQ(Dataset):
    def __init__(self, args, mode, word2id, rela2id, vocab_mapping, bert_tokenizer):
        super(PerQuestionDatasetMLPQ, self).__init__()
        self.bert_tokenizer = bert_tokenizer
        self.data_objs = self._get_data(args, mode, word2id, rela2id, vocab_mapping)

    def _get_data(self, args, mode, word2id, rela2id, vocab_mapping):
        data_objs = []
        if args.framework == 'UHop':
            file_path = U_PATH[args.dataset]
            print(file_path)
            with open(f'{file_path}/{mode}_data.txt', 'r') as f:
                for i, line in enumerate(f):
                    data = json.loads(line)
                    data = self._numericalize(data, word2id, rela2id, args.q_representation, 'UHop', vocab_mapping)
                    data_objs.append(data)
            print(f'\rreading line {len(data_objs)}')
            # data_objs = random.sample(data_objs, min(10000, len(data_objs)))
        elif args.framework == 'baseline':
            file_path = B_PATH[args.dataset.lower()]
            print(file_path)
            with open(file_path.replace('MODE', mode), 'r') as f:
                for i, line in enumerate(f):
                    print(f'\rreading line {i}', end='')
                    anses, candidates, question = line.strip().split('\t')
                    # modify because of 'noNegativeAnswer' in sq data
                    candidates = [[x, [], 0] for x in candidates.split() if x not in anses.split() and x!='noNegativeAnswer']
                    # modify for "#head_entity#" label in sq dataset
                    ques = question.replace('$ARG1', '').replace('$ARG2', '')
                    ques = ques.replace('<e>', 'TOPIC_ENTITY').replace('#head_entity#', 'TOPIC_ENTITY').strip()
                    for ans in anses.split():
                        data = (i, ques, [[[ans, [], 1]]+candidates])
                        data = self._numericalize(data, word2id, rela2id, args.q_representation, 'baseline')
                        data_objs.append(data)
        return data_objs
    def _numericalize(self, data, word2id, rela2id, q_representation, framework, vocab_mapping):
        index, ques, step_list = data[0], data[1], data[2]
        if q_representation == "bert":
            ques = self._bert_numericalize_str(ques)
        else:
            ques = self._numericalize_str(ques, word2id, [' '])
        if framework == 'baseline':
            tuples = []
            for t in step_list[0]:
                num_rela = self._numericalize_str(t[0], rela2id, ['.'])
                num_rela_text = self._numericalize_str(t[0], word2id, ['.', '_'])
                num_prev = [self._numericalize_str(prev, rela2id, ['.']) for prev in t[1]]
                num_prev_text = [self._numericalize_str(prev, word2id, ['.', '_']) for prev in t[1]]
                tuples.append((num_rela, num_rela_text, num_prev, num_prev_text, t[2]))
            new_step_list = tuples
        else:
            new_step_list = []
            for step in step_list:
                new_step = []
                for t in step:
                    num_rela = self._numericalize_rel(t[0], rela2id)
                    num_rela_text = self._numericalize_rel_text(t[0], word2id, vocab_mapping)
                    num_prev = [self._numericalize_rel(prev, rela2id) for prev in t[1]]
                    num_prev_text = [self._numericalize_rel_text(prev, word2id, vocab_mapping) for prev in t[1]]
                    new_step.append((num_rela, num_rela_text, num_prev, num_prev_text, t[2]))
                new_step_list.append(new_step)
        return index, ques, new_step_list
    def _numericalize_str(self, string, map2id, dilemeter):
        #print('original str:', string)
        if len(dilemeter) == 2:
            string = string.replace(dilemeter[1], dilemeter[0])
        dilemeter = dilemeter[0]
        tokens = string.strip().split(dilemeter)
        tokens = [map2id[x] if x in map2id else map2id['<unk>'] for x in tokens]
        #print('tokens:', tokens)
        return tokens
    def _numericalize_rel(self, string, map2id):
        #print('original str:', string)
        tokens = [string]
        tokens = [map2id[x] if x in map2id else map2id['<unk>'] for x in tokens]
        #print('tokens:', tokens)
        return tokens
    def _numericalize_rel_text(self, string, map2id, vocab_mapping):
        #print('original str:', string)
        string = vocab_mapping[string] if string in vocab_mapping else string
        new_string = ""
        for s in string:
            if s.isupper():
                new_string += " "
            new_string += s.lower()
        tokens = new_string.split(" ")
        tokens = [map2id[x] if x in map2id else map2id['<unk>'] for x in tokens]
        #print('tokens:', tokens)
        return tokens
    def _bert_numericalize_str(self, seq):
        tokens = self.bert_tokenizer.tokenize(seq)
        tokens = ['[CLS]'] + tokens + ['[SEP]']
        tokens = self.bert_tokenizer.convert_tokens_to_ids(tokens)
        return tokens
    def __len__(self):
        return len(self.data_objs)
    def __getitem__(self, index):
        return self.data_objs[index]


def load_lan_vocab(src, tag):
    src_text = []
    with open(src) as fin:
        for line in fin:
            src_text.append(line.strip())
    tag_text = []
    with open(tag) as fin:
        for line in fin:
            tag_text.append(line.strip())
    assert len(src_text) == len(tag_text)
    vocab_mapping = {src_text[i] : tag_text[i] for i in range(len(src_text))}
    return vocab_mapping


if __name__ == '__main__':
    with open('../data/WQ/main_exp/rela2id.json', 'r') as f:
        rela2id =json.load(f)
    word2id_path = '../data/glove.300d.word2id.json' 
    with open(word2id_path, 'r') as f:
        word2id = json.load(f)
    class ARGS():
        def __init__(self):
            self.dataset = 'wq'
            self.mode = 'train'
        pass
    args = ARGS()
    dataset = PerQuestionDataset(args, 'train', word2id, rela2id)
    print()
    print(0, dataset[100][0])
    print(1, dataset[100][1])
    print(2, dataset[100][2])
    print(len(dataset[100]))
