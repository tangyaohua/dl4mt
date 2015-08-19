import numpy
import cPickle as pkl

from nltk.tokenize import wordpunct_tokenize

from collections import OrderedDict

class TextIterator:
    def __init__(self, source, target, 
                 source_dict, target_dict, 
                 maxlen=100,
                 n_words_source=-1,
                 n_words_target=-1,
                 tau=-1):
        self.source = open(source, 'r')
        self.target = open(target, 'r')
        with open(source_dict, 'rb') as f:
            self.source_dict = pkl.load(f)
        with open(target_dict, 'rb') as f:
            self.target_dict = pkl.load(f)

        self.maxlen = maxlen

        self.n_words_source = n_words_source
        self.n_words_target = n_words_target
        self.tau=tau
        self.temp_target_dict = {}

        self.end_of_data = False

    def __iter__(self):
        return self

    def reset(self):
        self.source.seek(0)
        self.target.seek(0)

    def next(self):
        if self.end_of_data:
            self.end_of_data = False
            self.reset()
            raise StopIteration

        source = []
        target = []
        ii = 0

        word_freqs = set([0,1])

        try:
            while True:
                ss = self.source.readline()
                if ss == "":
                    raise IOError
                ss = ss.strip().split()
                ss = [self.source_dict[w] if w in self.source_dict else 1 for w in ss]
                if self.n_words_source > 0:
                    ss = [w if w < self.n_words_source else 1 for w in ss]

                if len(ss) > self.maxlen:
                    continue

                tt = self.target.readline()
                if tt == "":
                    raise IOError
                tt = tt.strip().split()
                if len(tt) > self.maxlen:
                    continue
                ttt=[]
                for w in tt:
                    if w in self.target_dict:
                        ind=self.target_dict[w]
                        ttt.append(ind)
                        if ind not in word_freqs:
                            word_freqs.add(ind)
                    else:
                        ttt.append(1)

                if self.n_words_target > 0:
                    ttt = [w if w < self.n_words_target else 1 for w in ttt]

                source.append(ss)
                target.append(ttt)

                if len(word_freqs)>self.tau-2:
                    break

        except IOError:
            self.end_of_data = True

        if len(source) <= 0 or len(target) <= 0:
            print 'too little sentences'
            self.end_of_data = False
            self.reset()
            raise StopIteration

        return source, target, word_freqs




