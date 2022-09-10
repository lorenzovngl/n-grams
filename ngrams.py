# -*- coding: utf-8 -*-,

# Usage: 	python ngrams.py [corpus_file] [type_of_ngrams] [words_to_generate]
# Example: 	python ngrams.py corpus.txt 3 30

from __future__ import division
import json, random
from nltk.util import ngrams
from nltk import word_tokenize
import os, sys

punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

# Assigns the probabilities to the n-grams
# P(w_i|w_(i-1)) = count(w_(i-1), w_i)/count(w_(i-1))
def prob(corpus, word, context):
	return corpus.count(context+' '+word)/corpus.count(context)

# Build the choice tree
def build_choice_tree(T, word, context, prob):
	level = T
	for token in context:
		if token not in level:
			level[token] = {'prob': 1}
		level = level[token]
	level[word] = {'prob': prob}
	return T

# Restituisce una posizione casuale pesata in una lista di probabilità
def rand(items, prob):
	r = random.random()*sum(prob)
	last = 0
	s = prob[0]
	for i in range(1, len(items)):
		if s<=r:
			s += prob[i]		
			last = i
	return last

# Generates a random sentence according to the choice tree and probability
def generate(T):
	t = T
	first = True
	output = ''
	words = 0
	while words < int(sys.argv[3]):
		l = []
		w = []
		for key in t:
			if key != 'prob':
				l.append(key)
				w.append(t[key]['prob'])
		c = rand(l, w)
		if not first and l[c] not in punctuations:
			output += ' '
		first = False
		if l[c] not in punctuations:
			words += 1
		output += l[c]
		t = T[l[c]]
	return output

with open(sys.argv[1], 'r') as f:
		data = f.read()
s_token = word_tokenize(data)
n = int(sys.argv[2])
sixgrams = list(set(ngrams(s_token, n)))
C = {}
if not os.path.exists('out'):
    os.makedirs('out')
with open('out/probabilities.txt', 'w') as f:
		f.write('')
for grams in sixgrams:
	p = prob(' '.join(s_token), grams[n-1], ' '.join(grams[:n-1]))
	with open('out/probabilities.txt', 'a') as f:
		f.write('P('+grams[n-1]+'|'+' '.join(grams[:n-1])+') = ' + str(p) + '\n')
	C = build_choice_tree(C, grams[n-1], grams[:n-1], p)
with open('out/tree.json', 'w') as f:
	f.write(json.dumps(C, indent=4, sort_keys=True))
with open('out/output.txt', 'w') as f:
	f.write(generate(C))
