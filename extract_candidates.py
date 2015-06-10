__author__ = 'rwechsler'


from corpus_reader import CorpusReader
import dawg
from collections import defaultdict
import cPickle as pickle
import numpy as np


def build_vocabulary(corpus, min_length=0):
    """
    Build prefix and suffix vocabulary.
    :param corpus: CorpusReader object
    :param min_length: minimum character length of words to be considered
    :return: prefix_vocabulary and suffix_vocabulary
    """

    prefix_vocab = set()
    suffix_vocab = set()
    for tokens in corpus:
        for tok in tokens:
            if len(tok) >= min_length:
                prefix_vocab.add(tok)
                suffix_vocab.add(tok[::-1])

    return prefix_vocab, suffix_vocab

def add_prefix_combinations(combinations, prefix_vocab, dawg_model, fugenlaute=[]):
    fugenlaute += [""]
    for word in prefix_vocab:
        for prefix in dawg_model.prefixes(word)[:-1]: # last word is the word itself
            rest = word[len(prefix):]
            # Consider fugenlaute
            for fl in fugenlaute:
                if rest.startswith(fl):
                    if rest[len(fl):].title() in dawg_model:
                        combinations[prefix].add((fl, rest[len(fl):].title()))
                        break
                    elif rest[len(fl):] in dawg_model:
                        combinations[prefix].add((fl, rest[len(fl):]))
                        break

    return

def add_suffix_combinations(combinations, suffix_vocab, lower_suffix_dawg_model, fugenlaute=[""]):
    fugenlaute = [fl[::-1] for fl in fugenlaute] + [""]
    for word in suffix_vocab:
        for suffix in lower_suffix_dawg_model.prefixes(word): # last word is the word itself
            rest = word[len(suffix):]
            # Consider fugenlaute
            for fl in fugenlaute:
                if rest.startswith(fl):
                    if rest[len(fl):] in suffix_vocab:
                        combinations[rest[len(fl):][::-1]].add((fl[::-1], suffix[::-1]))
                        break

    return

corpus = CorpusReader("data/news.2011.true.de.gz", max_limit=100000)

print "Building vocabulary ..."
prefix_vocab, suffix_vocab = build_vocabulary(corpus, min_length=4)
print "Building dawg models"
dawg_model = dawg.DAWG(prefix_vocab)
lower_suffix_dawg_model = dawg.DAWG(set(w.lower() for w in suffix_vocab))

print "Vocabulary size: ", len(prefix_vocab)


fugenlaute = ["en", "es", "s"] # priority list.

combinations = defaultdict(set)
print "Prefix pass ..."
add_prefix_combinations(combinations, prefix_vocab, dawg_model, fugenlaute=fugenlaute)
print "Suffix pass ..."
add_suffix_combinations(combinations, suffix_vocab, lower_suffix_dawg_model, fugenlaute=fugenlaute)

print "Pickling model ..."

pickle.dump(combinations, open("comb_model.p", "wb"))

# some statistics
for k, v in combinations.items()[:40]:
    print k, v


tuples = sorted([(k, len(v)) for k,v in combinations.items()], key= lambda tup: tup[1], reverse=True)
print "------"
print "Longest keys: "
for k, v in tuples[:40]:
    print k, v

keys, lengths = zip(*tuples)

print "----"
print "Keys: ", len(combinations)
print "Longest key: ", keys[np.argmax(lengths)], np.max(lengths)
print "Average length: ", np.mean(lengths)


