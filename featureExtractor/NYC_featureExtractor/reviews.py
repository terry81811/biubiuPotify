import io
from datetime import *
from time import *
import math

import sys
sys.path.append("../")
from utilities import *

####################
# reading files
####################


f_biz = io.open('../input/NYC/businessesIdMapping_nyc.tsv', 'r', encoding='utf8')
f_user = open('../input/NYC/user_id_mapping_all_nyc.tsv', 'r')
f_meta = open('../input/NYC/metadata_nyc.tsv', 'r')
f_content = io.open('../input/NYC/reviewContent_nyc.tsv', 'r', encoding='utf8')

# reading biz

bizs_lines = [line.rstrip('\n\r').split('\t') for line in f_biz]

bizs = {}

for biz in bizs_lines:
	bizs[biz[1]] = {
		'id': biz[0],
	}

print len(bizs)
print bizs['0']

# reading user

users = {}
user_lines = [line.rstrip('\n\r').split('\t') for line in f_user]

for user_line in user_lines:
	users[user_line[1]] = {
		'id': user_line[0],
		'neg': 0,
		'pos': 0,
	}

print len(users)
print users['100752']

# reading content

reviews = {}
content_lines = [line.rstrip('\n\r').split('\t') for line in f_content]

for i in range(len(content_lines)):
	content_line = content_lines[i]
	reviews[str(i)] = {
		'id': str(i),
		'text': content_line[3],
	}

# reading meta

meta_lines = [line.rstrip('\n\r').split('\t') for line in f_meta]

for i in range(len(meta_lines)):
	meta_line = meta_lines[i]
	reviews[str(i)]['user'] = users[meta_line[0]]['id']
	reviews[str(i)]['biz'] = bizs[meta_line[1]]['id']
	reviews[str(i)]['rating'] = float(meta_line[2])
	reviews[str(i)]['label'] = int(meta_line[3])
	reviews[str(i)]['date'] = datetime.strptime(meta_line[4], '%Y-%m-%d')

print len(reviews)
print reviews['0']


####################
# group by restaurants
####################

restaurants = {}

for k, v in bizs.iteritems():
	restaurants[v['id']] = {
		'reviews': [],
	}


for k, review in reviews.iteritems():
	restaurants[review['biz']]['reviews'].append(review)

# cnt = 0

# for k, v in restaurants.iteritems():
#  	cnt += len(v['reviews'])

# print cnt
# print len(reviews)

# print restaurants['King of Falafel & Shawarma']

####################
# getting features for reviews
####################

reviewsIdMap = reviews

# 1. rank
# 2. rank ratio
# 3. rank time frame

# 1-1. build a sorted date array with each restaurant
for k, v in restaurants.iteritems():
	dates = [review['date'] for review in v['reviews']]
	dates.sort()
	sorted = [datetime.strftime(ts, "%Y-%m-%d") for ts in dates]
	restaurants[k]['sorted_dates'] = sorted

	first_time = datetime.strptime(sorted[0], '%Y-%m-%d')
	last_time = datetime.strptime(sorted[-1], '%Y-%m-%d')

	first = mktime(first_time.timetuple())
	last = mktime(last_time.timetuple())
	restaurants[k]['first_date'] = first
	restaurants[k]['last_date'] = last


print ">>> anotating rank"
for k, v in reviewsIdMap.iteritems():

	# get reviews of the same restaurant this review reviewed
	numberOfReviews = len(restaurants[v['biz']]['reviews'])

	total = len(restaurants[v['biz']]['reviews'])
	rank = restaurants[v['biz']]['sorted_dates'].index(datetime.strftime(v['date'], "%Y-%m-%d"))
	duplicate = restaurants[v['biz']]['sorted_dates'].count(datetime.strftime(v['date'], "%Y-%m-%d"))

	# 1-2 rank
	reviewsIdMap[k]['rank'] = rank + (duplicate - 1) / 2

	# 1-3 rank ratio
	reviewsIdMap[k]['rank_ratio'] = (rank + (duplicate - 1) / 2) / float(total)

	# 1-4 rank time frame
	first = restaurants[v['biz']]['first_date']
	last = restaurants[v['biz']]['last_date']
	time = mktime(v['date'].timetuple())

	if time - first == 0:
		rank_time_frame = 0
	else:
		rank_time_frame = float(time - first) / (last - first)

	reviewsIdMap[k]['rank_time_frame'] = rank_time_frame



# 4. Rating deviation
print ">>> anotating rating deviation"

# 4-1. calculate avg rating for each product
for k, v in restaurants.iteritems():
	ratings = [review['rating'] for review in v['reviews']]
	restaurants[k]['avg_rating'] = float(sum(ratings)) / len(ratings)

# 4-2 calculate deviation
for k, v in reviewsIdMap.iteritems():
	reviewsIdMap[k]['rating_deviation'] = math.fabs(v['rating'] - restaurants[v['biz']]['avg_rating'])


# 5. Extremity of rating 
print ">>> anotating Extremity of rating "
for k, v in reviewsIdMap.iteritems():
	if v['rating'] > 3:
		reviewsIdMap[k]['ext_rating'] = 1
	else:
		reviewsIdMap[k]['ext_rating'] = 0


# 6. PCW Percentage of ALL-capitals words
# 7. PC Percentage of capital letters
# 8. L Review length in words
# 9. PP1 Ratio of 1st person pronouns
# 10. RES Ratio of exclamation sentences containing

# 11. pos Ratio of pos words (by sentiWordNet)
# 12. neg Ratio of neg words (by sentiWordNet)
# 13. SW Ratio of subjective words (by sentiWordNet)
# 14. OW Ratio of objective words (by sentiWordNet)

f_out = io.open('../output/NYC/review_features_nyc.tsv', 'w', encoding='utf8')

cnt = 0
for k, v in reviewsIdMap.iteritems():

	if cnt % 1000 == 0:
		print ">>> anotating review: " + str(cnt)
	cnt += 1

	tokens = tokenize(v['text'])
	L = len(tokens)
	if L == 0:
		L = 1

	PCW = float(countAllUpper(tokens)) / L
	PC = float(countCapital(v['text'])) / len(v['text'])
	onePP = float(count1PPWord(tokens)) / L


	sentences = sent_tokenize(v['text'])
	RES = float(countExclamations(sentences)) / len(sentences)

	# print ">>> PCW: " + str(PCW)
	# print ">>> PC: " + str(PC)
	# print ">>> L: " + str(L)
	# print ">>> 1-PP: " + str(onePP)
	
	reviewsIdMap[k]['L'] = L
	reviewsIdMap[k]['PCW'] = PCW
	reviewsIdMap[k]['PC'] = PC
	reviewsIdMap[k]['onePP'] = onePP
	reviewsIdMap[k]['RES'] = RES


	# sentiment analysis
	pos_tokens = nltk.pos_tag(tokenize(v['text'].lower()))
	(objCount, subCount, negScore, posScore) = getSentiment(nltk.pos_tag(tokens))

	reviewsIdMap[k]['posScore'] = float(posScore) / L
	reviewsIdMap[k]['negScore'] = float(negScore) / L

	if objCount + subCount == 0:
		reviewsIdMap[k]['SW'] = 0.0
		reviewsIdMap[k]['OW'] = 0.0
	else:
		reviewsIdMap[k]['SW'] = float(subCount) / (objCount + subCount)
		reviewsIdMap[k]['OW'] = float(objCount) / (objCount + subCount)


	out = []
	out.append(k)
	out.append(v['biz'])
	out.append(v['user'])
	out.append(str(v['rating']))
	out.append(str(datetime.strftime(v['date'], '%Y-%m-%d')))
	out.append(str(v['rank']))
	out.append(str(v['rank_ratio']))
	out.append(str(v['rank_time_frame']))
	out.append(str(v['rating_deviation']))
	out.append(str(v['ext_rating']))
	out.append(str(v['L']))
	out.append(str(v['PCW']))
	out.append(str(v['PC']))
	out.append(str(v['onePP']))
	out.append(str(v['RES']))
	out.append(str(v['posScore']))
	out.append(str(v['negScore']))
	out.append(str(v['SW']))
	out.append(str(v['OW']))
	out.append(str(v['label']))

	f_out.write("\t".join(out) + "\n")


	

