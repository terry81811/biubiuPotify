from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.corpus import sentiwordnet as swn
from nltk.tokenize import sent_tokenize

import collections # optional, but we found the collections.Counter object useful
import scipy.sparse as sp
import numpy as np
import math


# helper function
def isAllUpper(text):
	if text == text.upper():
		return True
	else:
		return False


def countAllUpper(tokens):
	return sum(1 for token in tokens if isAllUpper(token))


def countCapital(text):
	return sum(1 for c in text if c.isupper())


def is1PPWord(text):
	onePP = ['i', 'me', 'we', 'us', 'myself', 'ourselves', 'my', 'our', 'mine', 'ours']
	if text.lower() in onePP:
		return True
	else:
		return False


def count1PPWord(tokens):
	return sum(1 for token in tokens if is1PPWord(token))


def tokenize(text):
	return nltk.word_tokenize(text.encode('ascii', 'ignore').decode('ascii', 'ignore'))


def countExclamations(sentences):
	return sum(1 for sentence in sentences if "!" in sentence)

def getSentiment(tokens):

	tag = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'TO', 'UH', 'PDT', 'SYM', 'RP']
	noun = ['NN', 'NNS', 'NP', 'NPS']
	adj = ['JJ', 'JJR', 'JJS']
	pronoun = ['PP', 'PP$', 'WP', 'WP$']
	verb = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
	adverb = ['RB', 'RBR', 'RBS', 'WRB']


	objCount = 0
	subCount = 0

	negScore = 0
	posScore = 0

	for w in tokens:
		if not w[1] in tag:
			if w[1] in noun:
				pos_Char = 'n'
			elif w[1] in adj:
				pos_Char = 'a'
			elif w[1] in pronoun:
				pos_Char = 'p'
			elif w[1] in verb:
				pos_Char = 'v'
			elif w[1] in adverb:
				pos_Char = 'r'
			else:
				pos_Char = 'none'

			if pos_Char == 'none':
				try:
					s = swn.senti_synsets(w[0])
					scores = list(s)[0]

					negScore += scores.neg_score()
					posScore += scores.pos_score()

					if scores.obj_score > 0.5:
						objCount += 1
					elif scores.pos_score() + scores.neg_score() > 0.5:
						subCount += 1
				except:
					pass
					# print('Unexpected word: ' + str(w) + ", pos == none")
			else:
				try:
					s = swn.senti_synsets(w[0], pos_Char)
					scores=list(s)[0]

					negScore += scores.neg_score()
					posScore += scores.pos_score()

					if scores.obj_score() > 0.5:
						objCount += 1
					elif scores.pos_score() + scores.neg_score() > 0.5:
						subCount += 1
				except:
					pass
					# print('Unexpected word: ' + str(w))

	return (objCount, subCount, negScore, posScore)



def cosine_similarity(X):
	"""
	Return a matrix of cosine similarities.
	
	Args:
		X: sparse matrix of TFIDF scores or term frequencies
	
	Returns:
		M: dense numpy array of all pairwise cosine similarities.  That is, the 
		   entry M[i,j], should correspond to the cosine similarity between the 
		   ith and jth rows of X.
	"""

	print ">>> in cosine_similarity"

	K = X.get_shape()[0]

	# resArr = [[None for x in range(K)] for y in range(K)]

	resArr = np.zeros((K, K))

	print ">>> in cosine_similarity"

	# calculate length for each doc
	lengths = []

	print ">>> calculating length of a doc"
	for j in range(K):
		row = X.getrow(j)
		leng = row.dot(row.transpose()).toarray().tolist()[0][0]
		lengths.append(math.sqrt(leng))

	# print np.array(lengths)

	lengths = np.array(lengths)[:,None]
	print lengths.shape

	resArr = np.zeros((K, K))
	resArr = X.dot(X.transpose()).todense()
	print resArr.shape
	
	resArr = resArr / lengths
	resArr = resArr / lengths.T

	return resArr



def tfidf(docs):
	all_words = set([a for a in " ".join(docs).split(" ") if a != ""])
	all_words_dict = {k:i for i,k in enumerate(all_words)}
	word_counts = [collections.Counter([a for a in d.split(" ") if a != ""]) for d in docs]

	#condtruct term frequency matrix in COO form
	data = [a for wc in word_counts for a in wc.values()]
	rows = [i for i,wc in enumerate(word_counts) for a in wc.values()]
	cols = [all_words_dict[k] for wc in word_counts for k in wc.keys()]
	X = sp.coo_matrix((data, (rows,cols)), (len(docs), len(all_words)))

	#comput IDF and IFIDF terms
	idf = np.log(float(len(docs))/np.asarray((X>0).sum(axis=0))[0])
	return X*sp.diags(idf), list(all_words)



# print isAllUpper('ABC')
# print isAllUpper('aBC')
# print countAllUpper(['ABC', 'abc'])
# print countCapital('AbCdEf')
# print is1PPWord('I')
# print is1PPWord('you')
# print count1PPWord(['I', 'you', 'We'])

# str_test = "My wife and I made an unexpected overnight stay in Pittsburgh on our way home from Niagara Falls recently. After checking into our hotel, we hit up Yelp to find a great place to eat in the Steel City. I used the search filters and found Gaucho Parrilla by searching \"highest rating.\" As soon as I started looking at the pictures, it dawned on me that I had stalked their page within the past year because I had seen their restaurant named on the Yelp top 100 list (#7). We immediately made plans to head straight to Gaucho. After driving around the block a few times, I wasn't too sure if we would be able to find a parking spot for the massive SUV rental, but we were finally able to get a good spot on the street just down a bit.We loaded up the parking meter and started making our way towards Gaucho... as we got closer and closer, I could smell the meats cooking in all of their meaty glory. I wasn't particularly hungry that day, but the smells emanating from the place took care of that in no time. Upon entering, everyone was super friendly and very helpful when it came to introducing us to their menu and pointing out a couple of options that would be great for first time Gaucho-ers. We tried the meat platter (Beef, Chicken, and Sausage) as well as the pulled pork with caramelized onions (My personal favorite). I have to say, I would be hard pressed to remember a meal that I enjoyed more than the one we had that night... the flavors at Gaucho are on another level of amazingness. If you are anywhere near Pittsburgh, go out of your way to try Gaucho, you will not be disappointed."
# str_test = "So. Good. Other than the staff getting really perturbed with you if you aren't standing in the correct spot (due to long lines out the door), it's incredible. Note: get there early!Go with a group. Get everything. Share. You'll be really full halfway through but press on. You're welcome."
# tokens = tokenize(str_test.lower())
# (objCount, subCount, negScore, posScore) = getSentiment(nltk.pos_tag(tokens))
# print (objCount, subCount, negScore, posScore)

# print countExclamations(sent_tokenize(str_test))
# print countExclamations(["afdqsd!", "asdafasfq", "!asdafas"])
