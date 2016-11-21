# user_features.py do the following 

# arg[1]: userFeatureWithLabel 
# arg[2]: reviewFeatures 
# arg[3]: metadata (to get user-review relations)
# arg[4]: userFeature_aggrReview_WithLabel (output)

# E.G.

# arg[1]
# userId, MNR, PR, NR, avgRD, WRD, ERD, BST, ETG, RL, ACS, MCS, posLabelCount, negLabelCount, purity
# 923,1,0,0,0.95,0.95,-0,0,-0,44.667,0.0083904,0.025171,1,1,0.5

# arg[2]
# rank,RD,EXT,DEV,ETF,ISR,PCW,PC,L,PP1,RES,SW,OW,(F),DLU,DLB
# 210,1.0095,0,0,0,0,0,0.035714,0.03969,0,0,0.076923,0.92308,380.56,594.94

# arg[3] metadata
# reviewId userId rating label date
# 1	923	0	3.0	-1	2014-12-08

# arg[4]
# userId, avgRankPercent, ETFPercent, isSingletonPercent, avgPAllCap, avgRatioSub, avgRatioObj, avgRatioExc
# 923,0,0.0,0.0,0.0183188153846,1.00000007692,1.00000007692,0.11686


import sys
import collections

f = open(sys.argv[1], 'r')
users_lines = [line.rstrip('\n\r') for line in f]

f2 = open(sys.argv[2], 'r')
reviews_lines = [line.rstrip('\n\r') for line in f2]

f3 = open(sys.argv[3], 'r')
metadata_lines = [line.rstrip('\n\r') for line in f3]

users = collections.OrderedDict()

print len(metadata_lines)

for line in metadata_lines:
	parts = line.split('\t')
	user = {
		'metadata': line,
		'reviews': [],
	}

	users[parts[1]] = user

for line in metadata_lines:
	parts = line.split('\t')
	users[parts[1]]['reviews'].append(parts[0])	

for k, v in users.iteritems():

	sumRankPercent = 0
	sumETFPercent = 0
	sumIsSingletonPercent = 0
	sumPAllCap = 0
	sumRatioSub = 0
	sumRatioObj = 0
	sumRatioExc = 0

	for reviewId in v['reviews']:
		parts = reviews_lines[int(reviewId) - 1].split(',')
		
		# sumRankPercent
		# this require knowing the number of reviews of a product
		sumETFPercent += float(parts[4])
		sumIsSingletonPercent += float(parts[5])
		sumPAllCap += float(parts[6])
		sumRatioSub += float(parts[12])
		sumRatioSub += float(parts[11])
		sumRatioExc += float(parts[10])

	users[k]['avgRankPercent'] = 0
	users[k]['ETFPercent'] = sumETFPercent / len(v['reviews'])
	users[k]['isSingletonPercent'] = sumIsSingletonPercent / len(v['reviews'])
	users[k]['avgPAllCap'] = sumPAllCap / len(v['reviews'])
	users[k]['avgRatioSub'] = sumRatioSub / len(v['reviews'])
	users[k]['avgRatioObj'] = sumRatioSub / len(v['reviews'])
	users[k]['avgRatioExc'] = sumRatioExc / len(v['reviews'])


outputFile = open(sys.argv[4], 'w')

for k, v in users.iteritems():
	attrs = []
	attrs.append(k)
	attrs.append(str(v['avgRankPercent']))
	attrs.append(str(v['ETFPercent']))
	attrs.append(str(v['isSingletonPercent']))
	attrs.append(str(v['avgPAllCap']))
	attrs.append(str(v['avgRatioSub']))
	attrs.append(str(v['avgRatioObj']))
	attrs.append(str(v['avgRatioExc']))

	s = ','.join(attrs)

	outputFile.write(s + '\n')



