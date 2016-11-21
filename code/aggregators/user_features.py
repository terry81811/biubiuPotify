# user_features.py do the following 

# arg[1]: userLabels
# arg[2]: userFeatures
# arg[3]: userFeatureWithLabel (output)


# E.G.

# arg[1]
# userId, posCount, negCount, purity(asNeg)
# 923	0	39	1.0

# arg[2]
# MNR, PR, NR, avgRD, WRD, ERD, BST, ETG, RL, ACS, MCS
# 1,0,0,0.95,0.95,-0,0,0,40.5,0.012586,0.025171

# arg[3]
# userId, MNR, PR, NR, avgRD, WRD, ERD, BST, ETG, RL, ACS, MCS, posLabelCount, negLabelCount, purity
# 923,1,0,0,0.95,0.95,-0,0,-0,44.667,0.0083904,0.025171,1,1,0.5


import sys
import collections

f = open(sys.argv[1], 'r')
users_lines = [line.rstrip('\n\r') for line in f]

users = []

for line in users_lines:
	parts = line.split('\t')
	user = {
		'id': parts[0],
		'pos': parts[1],
		'neg': parts[2],
		'purity': parts[3]
	}
	users.append(user)

# print users

f2 = open(sys.argv[2], 'r')
userFeatures_lines = [line.rstrip('\n\r') for line in f2]

outputFile = open(sys.argv[3], 'w')

for i in range(0, len(userFeatures_lines)):
	s = users[i]['id'] + "," + userFeatures_lines[i] + "," + users[i]['pos'] + "," + users[i]['neg'] + "," + users[i]['purity'] + "\n"
	outputFile.write(s)

