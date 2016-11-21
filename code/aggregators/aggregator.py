# aggregator.py do the following 

# arg[1]: userLabels
# arg[2]: userFeatures
# arg[3]: reviewFeatures 
# arg[4]: metadata (to get user-review relations)
# arg[5]: userFeatures (output)

# E.G.

# arg[1]
# userId	posCount	negCount	purity
# 923	0	39	1.0

# arg[2]
# MNR,PR,NR,avgRD,WRD,ERD,BST,ETG,RL,ACS,MCS
# 0.04,1,0,0.0095238,0.0095238,-0,1,0,29,-1,-1

# arg[3]
# rank,RD,EXT,DEV,ETF,ISR,PCW,PC,L,PP1,RES,SW,OW,(F),DLU,DLB
# 210,1.0095,0,0,0,0,0,0.035714,0.03969,0,0,0.076923,0.92308,1,380.56,594.94

# arg[4] metadata
# ReviewId	UserId	ProductId	rating	label	date
# 1	923	0	3.0	-1	2014-12-08

# arg[5]
# userId, avgRankPercent, ETFPercent, isSingletonPercent, avgPAllCap, avgRatioSub, avgRatioObj, avgRatioExc
# 923,0,0.0,0.0,0.0183188153846,1.00000007692,1.00000007692,0.11686

import sys
import collections
import numpy as np

userLabelsFileName = "aggr_output/users_labels.tsv"
userFeaturesFileName = "aggr_input/userFeatures.csv"
reviewFeaturesFileName = "aggr_input/reviewFeatures.csv"
metadataFileName = "aggr_input/test_metadata.tsv"
userFeaturesOutputFileName = "aggr_output/userFeaturesOutput.csv"

f = open(userLabelsFileName, 'r')
userLabels = [line.rstrip('\n\r') for line in f]
userLabelsFields = userLabels[0]
userLabels = userLabels[1:]

print ">>> reading userLabels ... " + str(len(userLabels) - 1) + " lines"

f = open(userFeaturesFileName, 'r')
userFeatures = [line.rstrip('\n\r') for line in f]
userFeaturesFields = userFeatures[0]
userFeatures = userFeatures[1:]

print ">>> reading userFeatures ... " + str(len(userFeatures) - 1) + " lines"

f = open(reviewFeaturesFileName, 'r')
reviewFeatures = [line.rstrip('\n\r') for line in f]
reviewFeaturesFields = reviewFeatures[0]
reviewFeatures = reviewFeatures[1:]

print ">>> reading reviewFeatures ... " + str(len(reviewFeatures) - 1) + " lines"

f = open(metadataFileName, 'r')
metadata = [line.rstrip('\n\r') for line in f]
metadataFields = metadata[0]
metadata = metadata[1:]

print ">>> reading metadata ... " + str(len(metadata) - 1) + " lines"

# build userFeaturesOutput
users = collections.OrderedDict()

for line in userLabels:
	parts = line.split('\t')
	user = {
		'purity': parts[3],
		'posCount': parts[1],
		'negCount': parts[2],
		'reviews': [],
		'features': [],
	}

	users[parts[0]] = user

print ">>> built users ... " + str(len(users)) + " instances"
print users['923']

# build user to review relations
for line in metadata:
	parts = line.split('\t')
	users[parts[1]]['reviews'].append(map(float, reviewFeatures[int(parts[0]) - 1].split(",")))	


# convert reviews from list of list of strings to float
for userId, user in users.iteritems():
	user['reviews'] = np.array(user['reviews'])

print ">>> built user to review relations, stored reviews as np array... "
print len(users['930']['reviews'])


# feature aggregations
featureLabelNames = []

# Rank
featureLabelNames.extend(["MinRank", "AvgRank", "MedianRank"])
for userId, user in users.iteritems():
	user['features'].append(user['reviews'][:, 0].min())
	user['features'].append(user['reviews'][:, 0].mean())
	user['features'].append(np.median(user['reviews'][:, 0]))

# RD
featureLabelNames.extend(["AvgRD", "MaxRD", "StdRD"])
for userId, user in users.iteritems():
	user['features'].append(user['reviews'][:, 1].mean())
	user['features'].append(user['reviews'][:, 1].max())
	user['features'].append(user['reviews'][:, 1].std())

# EXT
featureLabelNames.extend(["EXTPercent", "EXTCount"])
for userId, user in users.iteritems():
	user['features'].append(user['reviews'][:, 2].mean())
	user['features'].append(user['reviews'][:, 2].sum())

# DEV
featureLabelNames.extend(["DEVPercent", "DEVCount"])
for userId, user in users.iteritems():
	user['features'].append(user['reviews'][:, 3].mean())
	user['features'].append(user['reviews'][:, 3].sum())

# ETF
featureLabelNames.extend(["ETFPercent", "ETFCount"])
for userId, user in users.iteritems():
	user['features'].append(user['reviews'][:, 4].mean())
	user['features'].append(user['reviews'][:, 4].sum())

# ISR
featureLabelNames.extend(["ISRPercent", "ISRCount"])
for userId, user in users.iteritems():
	user['features'].append(user['reviews'][:, 5].mean())
	user['features'].append(user['reviews'][:, 5].sum())

# PCW
featureLabelNames.extend(["AvgPCW", "MaxPCW"])
for userId, user in users.iteritems():
	user['features'].append(user['reviews'][:, 6].mean())
	user['features'].append(user['reviews'][:, 6].max())

# PC
featureLabelNames.extend(["MinPC", "MaxPC", "StdPC", "AvgPC"])
for userId, user in users.iteritems():
	user['features'].append(user['reviews'][:, 7].mean())
	user['features'].append(user['reviews'][:, 7].min())
	user['features'].append(user['reviews'][:, 7].max())
	user['features'].append(user['reviews'][:, 7].std())

# RL
featureLabelNames.extend(["MaxRL", "MinRL", "StdRL", "AvgRL"])
for userId, user in users.iteritems():
	user['features'].append(user['reviews'][:, 8].max())
	user['features'].append(user['reviews'][:, 8].min())
	user['features'].append(user['reviews'][:, 8].std())
	user['features'].append(user['reviews'][:, 8].mean())

# PP1
featureLabelNames.extend(["AvgPP1", "MedianPP1", "MaxPP1"])
for userId, user in users.iteritems():
	user['features'].append(user['reviews'][:, 9].mean())
	user['features'].append(np.median(user['reviews'][:, 9]))
	user['features'].append(user['reviews'][:, 9].max())

# RES
featureLabelNames.extend(["AvgRES", "MedianRES", "MaxRES", "MinRES", "StdRES"])
for userId, user in users.iteritems():
	user['features'].append(user['reviews'][:, 10].mean())
	user['features'].append(np.median(user['reviews'][:, 10]))
	user['features'].append(user['reviews'][:, 10].max())
	user['features'].append(user['reviews'][:, 10].min())
	user['features'].append(user['reviews'][:, 10].std())


# SW
featureLabelNames.extend(["AvgSW", "MedianSW", "MaxSW", "MinSW", "StdSW"])
for userId, user in users.iteritems():
	user['features'].append(user['reviews'][:, 11].mean())
	user['features'].append(np.median(user['reviews'][:, 11]))
	user['features'].append(user['reviews'][:, 11].max())
	user['features'].append(user['reviews'][:, 11].min())
	user['features'].append(user['reviews'][:, 11].std())

# OW
featureLabelNames.extend(["AvgOW", "MedianOW", "MaxOW", "MinOW", "StdOW"])
for userId, user in users.iteritems():
	user['features'].append(user['reviews'][:, 12].mean())
	user['features'].append(np.median(user['reviews'][:, 12]))
	user['features'].append(user['reviews'][:, 12].max())
	user['features'].append(user['reviews'][:, 12].min())
	user['features'].append(user['reviews'][:, 12].std())


# F
featureLabelNames.extend(["AvgF", "MaxF", "MedianF"])
for userId, user in users.iteritems():
	user['features'].append(user['reviews'][:, 13].mean())
	user['features'].append(np.median(user['reviews'][:, 13]))
	user['features'].append(user['reviews'][:, 13].max())

# Dlu
featureLabelNames.extend(["MinDlu", "AvgDlu"])
for userId, user in users.iteritems():
	user['features'].append(user['reviews'][:, 14].mean())
	user['features'].append(user['reviews'][:, 14].min())

# Dlb
featureLabelNames.extend(["MinDlb", "AvgDlb"])
for userId, user in users.iteritems():
	user['features'].append(user['reviews'][:, 15].mean())
	user['features'].append(user['reviews'][:, 15].min())

# out put to file
outputFile = open(userFeaturesOutputFileName, 'w')
outputFile.write("userId" + "," + ",".join(featureLabelNames) + "\n")

for userId, user in users.iteritems():
	outputFile.write(userId + "," + ",".join(map(str, user['features'])) + "\n")

print len(featureLabelNames)
print len(users['923']['features'])

