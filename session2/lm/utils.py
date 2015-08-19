#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

from vocab import Vocab
from lmdataset import LMDataset
from deepy.dataset import BunchSequences

import cPickle as pkl


logging.basicConfig(level=logging.INFO)

# resource_dir = os.path.abspath(os.path.dirname(__file__)) + os.sep + "resources"
resource_dir = '/home/tangyaohua/dl4mt/data/larger.corpus/'
# resource_dir = '/home/tangyh/Dropbox/PycharmProjects/dl4mt/session2/lm/resources/'

def load_data(small=True, char_based=False, batch_size=20, vocab_size=10000, history_len=5, max_tokens=50, null_mark=False):
    vocab_path = os.path.join(resource_dir, "ptb.train.txt")
    valid_path = os.path.join(resource_dir, "ptb.valid.txt")
    if small:
        train_path = os.path.join(resource_dir, "ptb.train.10k.txt")
    else:
        train_path = os.path.join(resource_dir, "ptb.train.txt")
    vocab = Vocab(char_based=char_based, null_mark=null_mark)
    vocab.load(vocab_path, max_size=vocab_size)

    lmdata = LMDataset(vocab, train_path, valid_path, history_len=-1, char_based=char_based, max_tokens=max_tokens)
    batch = BunchSequences(lmdata, batch_size=batch_size, fragment_length=history_len)
    return vocab, batch


def load_datagivendict(dictpath, small=True, char_based=False, batch_size=20, vocab_size=10000, history_len=5, max_tokens=50, null_mark=False):
    with open(dictpath, 'rb') as f:
            vocab = pkl.load(f)

    valid_path = os.path.join(resource_dir, "testtrg")
    if small:
        train_path = os.path.join(resource_dir, "traintrg")
    else:
        train_path = os.path.join(resource_dir, "traintrg")

    lmdata = LMDataset(vocab, train_path, valid_path, history_len=-1, char_based=char_based, max_tokens=max_tokens)
    batch = BunchSequences(lmdata, batch_size=batch_size, fragment_length=history_len)
    return vocab, batch