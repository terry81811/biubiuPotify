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
# print reviewsIdMap['aVT6N0mvnM5vmr2_igf1QQ']

text = reviewsIdMap['aVT6N0mvnM5vmr2_igf1QQ']['text']

docs_text = [" ".join(tokenize(v['text'])) for k, v in reviewsIdMap.iteritems()]

ks = [k for k, v in reviewsIdMap.iteritems()]

print len(docs_text)

print ">>> building tfidf features for docs"
(tfidf, all_words) = tfidf(docs_text)
print len(all_words)
print tfidf.shape

print ">>> computing pairwise cos-simiarity using tfidf features"
cosine_similarity(tfidf[0:10,])

# print M.shape
# print M


f_out = io.open('output/review_cos_sim_key.tsv', 'w', encoding='utf8')
f_out.write("\n".join(ks) + "\n")


# f_out = open('output/review_cos_sim.tsv', 'w')

# for i in range(M.shape[0]):
#     # print M[i]
#     # print M[i].shape
#     # print M[i].tolist()[0]

#     f_out.write("\t".join(map(str,M[i].tolist()[0])) + "\n")


# np.savetxt("output/review_cos_sim.tsv", M, delimiter="\t", fmt='%1.4f')


