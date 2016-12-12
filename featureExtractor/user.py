import io
from collections import Counter
import numpy


# getting users

f_biz = io.open('output/restaurant_features.tsv', 'r', encoding='utf8')
f_user = io.open('input/user_id_mapping_all.tsv', 'r', encoding='utf8')
f_reviews = io.open('output/review_features.tsv', 'r', encoding='utf8')

bizs_parts = [line.rstrip('\n\r').split('\t') for line in f_biz]
users_parts = [line.rstrip('\n\r').split('\t') for line in f_user]
reviews = [line.rstrip('\n\r').split('\t') for line in f_reviews]

print len(users_parts)

####################
# build restaurant id map
####################

bizs = {}

for bizs_part in bizs_parts:
	bizs[bizs_part[0]] = bizs_part[1:]

print bizs['mccormick-and-schmicks-pittsburgh-2']

####################
# group review by users
####################

# k	numRecR	numNonRecR	numR	
users = {}

for users_part in users_parts:
	users[users_part[1]] = {
		'reviews': [],
		'numRecR': int(users_part[2]),
		'numNonRecR': int(users_part[3]),
		'numR': int(users_part[2]) + int(users_part[3])
	}


for review in reviews:
	users[review[2]]['reviews'].append(review)


####################
# getting labels
####################

for k, v in users.iteritems():
	users[k]['fraction'] = float(users[k]['numNonRecR']) / users[k]['numR']
	res_fractions = [float(bizs[r[1]][-1]) for r in v['reviews']]
	users[k]['res_fractions'] = float(sum(res_fractions)) / len(res_fractions)
	
print users['We1kda5rqra8ClvV34Od4A']


####################
# getting features
####################

f_out = io.open('output/user_features.tsv', 'w', encoding='utf8')

cnt = 0

print len(users)

for k, v in users.iteritems():

	# print k
	if cnt % 1000 == 0:
		print ">>> annotating users: " + str(cnt)
	cnt += 1

	ratings = [float(review[3]) for review in v['reviews']]
	dateString = [review[4] for review in v['reviews']]
	ranks = [float(review[5]) for review in v['reviews']]
	rank_ratio = [float(review[6]) for review in v['reviews']]
	rank_time_frame = [float(review[7]) for review in v['reviews']]
	rating_deviation = [float(review[8]) for review in v['reviews']]
	ext_rating = [float(review[9]) for review in v['reviews']]
	L = [float(review[10]) for review in v['reviews']]
	PCW = [float(review[11]) for review in v['reviews']]
	PC = [float(review[12]) for review in v['reviews']]
	onePP = [float(review[13]) for review in v['reviews']]
	RES = [float(review[14]) for review in v['reviews']]
	posScore = [float(review[15]) for review in v['reviews']]
	negScore = [float(review[16]) for review in v['reviews']]
	SW = [float(review[17]) for review in v['reviews']]
	OW = [float(review[18]) for review in v['reviews']]
	labels = [float(review[19]) for review in v['reviews']]

	users[k]['numRecR'] = sum(1 for review in v['reviews'] if review[-1] == '1')
	users[k]['numNonRecR'] = sum(1 for review in v['reviews'] if review[-1] == '-1')
	users[k]['numR'] = len(v['reviews'])
	users[k]['avgRating'] = float(sum(ratings)) / len(ratings)
	users[k]['posRatingRatio'] = float(sum(1 for rating in ratings if rating > 3)) / len(ratings)
	users[k]['negRatingRatio'] = float(sum(1 for rating in ratings if rating < 3)) / len(ratings)

	most_common, num_most_common = Counter(dateString).most_common(1)[0]
	users[k]['maxRDay'] = num_most_common

	# ranks
	users[k]['avgRanks'] = float(sum(ranks)) / len(ranks)
	users[k]['minRanks'] = min(ranks)
	users[k]['avgRankRatio'] = float(sum(rank_ratio)) / len(rank_ratio)
	users[k]['minRankRatio'] = min(rank_ratio)
	users[k]['avgRankTimeFrame'] = float(sum(rank_time_frame)) / len(rank_time_frame)
	users[k]['minRankTimeFrame'] = min(rank_time_frame)

	users[k]['avgRD'] = float(sum(rating_deviation)) / len(rating_deviation)
	users[k]['maxRD'] = max(rating_deviation)

	users[k]['extRatingRatio'] = float(sum(1 for rating in ratings if rating == 1) + sum(1 for rating in ratings if rating == 5)) / len(ratings)

	users[k]['avgL'] = float(sum(L)) / len(L)
	users[k]['stdL'] = numpy.std(L)

	users[k]['avgPCW'] = float(sum(PCW)) / len(PCW)
	users[k]['maxPCW'] = max(PCW)
	users[k]['avgPC'] = float(sum(PC)) / len(PC)
	users[k]['maxPC'] = max(PC)
	users[k]['avgOnePP'] = float(sum(onePP)) / len(onePP)
	users[k]['maxOnePP'] = max(onePP)
	users[k]['avgRES'] = float(sum(RES)) / len(RES)
	users[k]['maxRES'] = max(RES)

	users[k]['avgPosScore'] = float(sum(posScore)) / len(posScore)
	users[k]['maxPosScore'] = max(posScore)
	users[k]['avgNegScore'] = float(sum(negScore)) / len(negScore)
	users[k]['maxNegScore'] = max(negScore)
	users[k]['avgSW'] = float(sum(SW)) / len(SW)
	users[k]['maxSW'] = max(SW)
	users[k]['avgOW'] = float(sum(OW)) / len(OW)
	users[k]['maxOW'] = max(OW)

	out = []
	out.append(k)
	out.append(str(v['numRecR']))
	out.append(str(v['numNonRecR']))
	out.append(str(v['numR']))
	out.append(str(v['avgRating']))
	out.append(str(v['posRatingRatio']))
	out.append(str(v['negRatingRatio']))
	out.append(str(v['maxRDay']))

	out.append(str(v['avgRanks']))
	out.append(str(v['minRanks']))
	out.append(str(v['avgRankRatio']))
	out.append(str(v['minRankRatio']))
	out.append(str(v['avgRankTimeFrame']))
	out.append(str(v['minRankTimeFrame']))

	out.append(str(v['avgRD']))
	out.append(str(v['maxRD']))

	out.append(str(v['extRatingRatio']))

	out.append(str(v['avgL']))
	out.append(str(v['stdL']))

	out.append(str(v['avgPCW']))
	out.append(str(v['maxPCW']))
	out.append(str(v['avgPC']))
	out.append(str(v['avgPC']))
	out.append(str(v['avgOnePP']))
	out.append(str(v['maxOnePP']))
	out.append(str(v['avgRES']))
	out.append(str(v['maxRES']))

	out.append(str(v['avgPosScore']))
	out.append(str(v['maxPosScore']))
	out.append(str(v['avgNegScore']))
	out.append(str(v['maxNegScore']))
	out.append(str(v['avgSW']))
	out.append(str(v['maxSW']))
	out.append(str(v['avgOW']))
	out.append(str(v['maxOW']))

	out.append(str(v['fraction']))
	out.append(str(v['res_fractions']))

	f_out.write("\t".join(out) + "\n")


