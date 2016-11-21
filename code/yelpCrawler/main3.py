from yelpAPI import *
import io, time, json
import sys
from collections import OrderedDict

#####################################
# get viewed restaurants by the 35158 users extracted from 1000 restaurants
#####################################


offset = sys.argv[1]

# load 1000 restaurant in Pittsburgh
oldBiz = set()
f = open('outputData/businessesIdMapping.tsv', 'r')
businessLines = [line.rstrip('\n\r') for line in f]

print len(businessLines)

for line in businessLines:
	oldBiz.add(line.split("\t")[1])

# print oldBiz
print len(oldBiz)

f = open('outputData/user_id_mapping_all.tsv', 'r')
userLines = [line.rstrip('\n\r') for line in f]

newBiz = OrderedDict()

for line in userLines[int(offset): int(offset) + 100]:
	parts = line.split("\t")

	businesses = getBizFromUserPage(parts[1])
	print ">>> " + parts[0] + "  extracted " + str(len(businesses)) + " from user: " + parts[1]
	for biz in businesses:
		if biz not in oldBiz:
			newBiz[biz] = parts[1]

print len(newBiz)


cnt = 1
f_newBiz = open('outputData/newBiz_' + offset + '.tsv', 'w')
for k, v in newBiz.iteritems():
	f_newBiz.write(str(cnt) + "\t" + v + "\t" + k + "\n")
	cnt += 1
