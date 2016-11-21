from yelpAPI import *
import io, time, json
import sys
from collections import OrderedDict

#####################################
# aggregate subset files into three files 
# re-number the reviews
# aggregate userId mapping into one bigger user file
# number users and update metadata
# 1. review content
# 2. metadata
# 3. userId mapping
#####################################

# aggregate users

def aggregateUsers():
	users = OrderedDict()

	countAllUsers = 0
	print ">>> aggregating users: "

	for i in range(10):

		f = open('outputData/user_id_mapping_' + str(i * 100) + '.tsv', 'r')
		lines = [line.rstrip('\n\r') for line in f]
		print ">>> FILE: " + str(i * 100) + " COUNT: " + str(len(lines))
		countAllUsers += len(lines)

		for line in lines:
			parts = line.split("\t")
			# print parts[1]

			if parts[1] not in users:
				users[parts[1]] = [int(parts[2]), int(parts[3])]
			else:
				users[parts[1]][0] += int(parts[2])
				users[parts[1]][1] += int(parts[3])


	print ">>> total number of users: " + str(len(users)) + " ...writing to file"

	f_userIdMapping = open('outputData/user_id_mapping_all.tsv', 'w')
	cnt = 1

	for k,v in users.iteritems():
		f_userIdMapping.write(str(cnt) + "\t" + str(k) + "\t" + str(v[0]) + "\t" + str(v[1]) + "\n")
		cnt += 1


def aggregateReviewMetaData():
	print ">>> aggregating reviews meta: "
	f_metaData = open('outputData/metaData_all.tsv', 'w')

	cnt = 1
	for i in range(10):
		f = open('outputData/metaData_' + str(i * 100) + '.tsv', 'r')
		lines = [line.rstrip('\n\r') for line in f]
		print ">>> FILE: " + str(i * 100) + " COUNT: " + str(len(lines))

		for line in lines:
			parts = line.split("\t")
			items = parts[1:5]
			date = parts[5].replace("Updatedreview", "").split("/")

			items.insert(0, str(cnt))
			items.append(date[2] + "-" + date[0] + "-" + date[1])
			cnt += 1

			f_metaData.write("\t".join(items) + "\n")


def aggregateReviewContents():
	print ">>> aggregating reviews contents: "
	f_reviewContent = open('outputData/reviews_content_all.tsv', 'w')

	cnt = 1
	for i in range(10):
		f = open('outputData/reviews_content_' + str(i * 100) + '.tsv', 'r')
		lines = [line.rstrip('\n\r') for line in f]
		print ">>> FILE: " + str(i * 100) + " COUNT: " + str(len(lines))

		for line in lines:
			parts = line.split("\t", 1)
			f_reviewContent.write(str(cnt) + "\t" + parts[1] + "\n")
			cnt += 1


