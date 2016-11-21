# user_purity.py do the following 

# arg[1]: review metafata
# arg[2]: users (output)

# E.G.

# arg[1]
# reviewId userId rating, label, date
# 1	923	0	3.0	-1	2014-12-08

# arg[2]
# userId, posCount, negCount, purity(asNeg)
# 923	0	39	1.0

import sys
import collections

f = open(sys.argv[1], 'r')
content = [line.rstrip('\n\r') for line in f]

users = collections.OrderedDict()

for line in content:

	parts = line.split('\t')
	userId = parts[1]

	if userId not in users:
		users[userId] = { 'pos': 0, 'neg': 0}

	if parts[4] == "1":
		users[userId]['pos'] += 1
	elif parts[4] == "-1":
		users[userId]['neg'] += 1


f2 = open(sys.argv[2], 'w')


for k, v in users.iteritems():
	f2.write(k + '\t' + str(v['pos']) + '\t' + str(v['neg']) + '\t' + str(float(v['neg']) / (v['pos'] + v['neg'])) + '\n')

