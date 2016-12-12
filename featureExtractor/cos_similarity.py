import io
from datetime import *
from time import *
import math
from utilities import *
import numpy as np

#####################
# main
#####################


f_content = io.open('input/reviews_content_all.tsv', 'r', encoding='utf8')
f_meta = open('input/metaData_all.tsv', 'r')
f_biz = io.open('input/businessesIdMapping.tsv', 'r', encoding='utf8')


bizs = [line.rstrip('\n\r').split('\t')[1] for line in f_biz]

reviews = {}
content_lines = [line.rstrip('\n\r').split('\t') for line in f_content]

for content_line in content_lines:
    reviews[content_line[0]] = {
        'id': content_line[1],
        'text': content_line[2],
    }

meta_lines = [line.rstrip('\n\r').split('\t') for line in f_meta]


for meta_line in meta_lines:

    reviews[meta_line[0]]['user'] = meta_line[1]
    reviews[meta_line[0]]['biz'] = int(meta_line[2])
    reviews[meta_line[0]]['rating'] = float(meta_line[3])
    reviews[meta_line[0]]['label'] = int(meta_line[4])
    reviews[meta_line[0]]['date'] = datetime.strptime(meta_line[5], '%Y-%m-%d')

reviewsIdMap = {}

for k, v in reviews.iteritems():
    reviewsIdMap[v['id']] = {
        'text': v['text'],
        'user': v['user'],
        'biz': bizs[int(v['biz']) - 1],
        'rating': v['rating'],
        'label': v['label'],
        'date': v['date'],
    }

print len(reviewsIdMap)

text = reviewsIdMap['aVT6N0mvnM5vmr2_igf1QQ']['text']

docs_text = [" ".join(tokenize(v['text'])) for k, v in reviewsIdMap.iteritems()]

ks = [k for k, v in reviewsIdMap.iteritems()]

print ">>> building tfidf features for docs"
(tfidf, all_words) = tfidf(docs_text)

print ">>> computing pairwise cos-simiarity using tfidf features"
cosine_similarity(tfidf[0:10,])


f_out = io.open('output/review_cos_sim_key.tsv', 'w', encoding='utf8')
f_out.write("\n".join(ks) + "\n")




