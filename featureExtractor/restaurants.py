import io
from collections import Counter
import numpy

####################
# reading files
####################

f_biz = io.open('input/businessesIdMapping.tsv', 'r', encoding='utf8')
f_reviews = io.open('output/review_features.tsv', 'r', encoding='utf8')

bizs = [line.rstrip('\n\r').split('\t')[1] for line in f_biz]
reviews = [line.rstrip('\n\r').split('\t') for line in f_reviews]


####################
# group by restaurants
####################

restaurants = {}

for biz in set(bizs):
	restaurants[biz] = {
		'reviews': [],
	}

cnt = 0
for review in reviews:
	restaurants[review[1]]['reviews'].append(review)
	# if review[-1] == 1

f_out = io.open('output/restaurant_features.tsv', 'w', encoding='utf8')

for k, v in restaurants.iteritems():

	print ">>> annotating restaurant: " + k

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

	restaurants[k]['numRecR'] = sum(1 for review in v['reviews'] if review[-1] == '1')
	restaurants[k]['numNonRecR'] = sum(1 for review in v['reviews'] if review[-1] == '-1')
	restaurants[k]['numR'] = len(v['reviews'])
	restaurants[k]['avgRating'] = float(sum(ratings)) / len(ratings)
	restaurants[k]['posRatingRatio'] = float(sum(1 for rating in ratings if rating > 3)) / len(ratings)
	restaurants[k]['negRatingRatio'] = float(sum(1 for rating in ratings if rating < 3)) / len(ratings)

	most_common, num_most_common = Counter(dateString).most_common(1)[0]
	restaurants[k]['maxRDay'] = num_most_common

	# restaurants[k]['EN'] = 


	# ranks
	# restaurants[k]['avgRanks'] = float(sum(ranks)) / len(ranks)
	# restaurants[k]['minRanks'] = min(ranks)
	# restaurants[k]['avgRankRatio'] = float(sum(rank_ratio)) / len(rank_ratio)
	# restaurants[k]['minRankRatio'] = min(rank_ratio)
	# restaurants[k]['avgRankTimeFrame'] = float(sum(rank_time_frame)) / len(rank_time_frame)
	# restaurants[k]['minRankTimeFrame'] = min(rank_time_frame)

	restaurants[k]['avgRD'] = float(sum(rating_deviation)) / len(rating_deviation)
	restaurants[k]['maxRD'] = max(rating_deviation)

	restaurants[k]['extRatingRatio'] = float(sum(1 for rating in ratings if rating == 1) + sum(1 for rating in ratings if rating == 5)) / len(ratings)

	restaurants[k]['avgL'] = float(sum(L)) / len(L)
	restaurants[k]['stdL'] = numpy.std(L)

	restaurants[k]['avgPCW'] = float(sum(PCW)) / len(PCW)
	restaurants[k]['maxPCW'] = max(PCW)
	restaurants[k]['avgPC'] = float(sum(PC)) / len(PC)
	restaurants[k]['maxPC'] = max(PC)
	restaurants[k]['avgOnePP'] = float(sum(onePP)) / len(onePP)
	restaurants[k]['maxOnePP'] = max(onePP)
	restaurants[k]['avgRES'] = float(sum(RES)) / len(RES)
	restaurants[k]['maxRES'] = max(RES)

	restaurants[k]['avgPosScore'] = float(sum(posScore)) / len(posScore)
	restaurants[k]['maxPosScore'] = max(posScore)
	restaurants[k]['avgNegScore'] = float(sum(negScore)) / len(negScore)
	restaurants[k]['maxNegScore'] = max(negScore)
	restaurants[k]['avgSW'] = float(sum(SW)) / len(SW)
	restaurants[k]['maxSW'] = max(SW)
	restaurants[k]['avgOW'] = float(sum(OW)) / len(OW)
	restaurants[k]['maxOW'] = max(OW)

	restaurants[k]['fraction'] = float(restaurants[k]['numNonRecR']) / restaurants[k]['numR']

	out = []
	out.append(k)
	out.append(str(v['numRecR']))
	out.append(str(v['numNonRecR']))
	out.append(str(v['numR']))
	out.append(str(v['avgRating']))
	out.append(str(v['posRatingRatio']))
	out.append(str(v['negRatingRatio']))
	out.append(str(v['maxRDay']))

	# out.append(str(v['avgRanks']))
	# out.append(str(v['minRanks']))
	# out.append(str(v['avgRankRatio']))
	# out.append(str(v['minRankRatio']))
	# out.append(str(v['avgRankTimeFrame']))
	# out.append(str(v['minRankTimeFrame']))

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

	f_out.write("\t".join(out) + "\n")
	
