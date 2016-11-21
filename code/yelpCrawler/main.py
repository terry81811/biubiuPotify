from yelpAPI import *
import io, time, json
import sys


#####################################
# load "recommended" and "non-recommended" reviews for all 
# restaurants given in a file, "argv = subset"
# generate three files
# 1. review content
# 2. metadata
# 3. userId mapping
#####################################


# load 1000 restaurants in Pittsburgh
client = authenticate("inputData/authenticate.json")
businesses = all_restaurants(client, 'Pittsburgh')

print ">>> get restaurants. count: " + str(len(businesses))

cnt = 1
f = io.open('outputData/businessesIdMapping.tsv', 'w', encoding='utf8')
for business in businesses:
	f.write(str(cnt) + "\t" + business.id + "\n")
	cnt += 1


subset = sys.argv[1]
print ">>> subset: " + str(subset)

f_reviews_content = io.open('outputData/reviews_content_' + subset + '.tsv', 'w', encoding='utf8')
f_userIdMapping = io.open('outputData/user_id_mapping_' + subset + '.tsv', 'w', encoding='utf8')
f_metaData = io.open('outputData/metaData_' + subset + '.tsv', 'w', encoding='utf8')

userIdDict = {}

# read 1000 restaurants in Pittsburgh

f = open('outputData/businessesIdMapping.tsv', 'r')
businessLines = [line.rstrip('\n\r') for line in f]

cnt = 1

for businessLine in businessLines[int(subset): int(subset) + 100]:

	businessId = businessLine.split('\t')[0]

	print ">>> " + businessId + " extracting recommended reviews from: " + businessLine.split('\t')[1]
	url = 'https://www.yelp.com/biz/' + businessLine.split('\t')[1]
	reviews = extract_reviews(url)
	print ">>> extrated " + str(len(reviews)) + " from " + businessLine.split('\t')[1]


	for review in reviews:

		# added user to user set
		if review['user_id'] not in userIdDict:
			userIdDict[review['user_id']] = {'pos': 0, 'neg': 1}
		else:
			userIdDict[review['user_id']]['neg'] += 1

		f_reviews_content.write(str(cnt) + "\t" + review['review_id'] + "\t" + review['text'] + "\n")
		f_metaData.write(str(cnt) + "\t" + review['user_id'] + "\t" + businessId + "\t" + str(review['rating']) + "\t" + "1\t" + review['date'] + "\n")
		cnt += 1


	print ">>> " + businessId + "  extracting non-recommended reviews from: " + businessLine.split('\t')[1]
	url = '/not_recommended_reviews/' + businessLine.split('\t')[1]
	reviews = extract_unrecommend_reviews(url)
	print ">>> extrated " + str(len(reviews)) + " from " + businessLine.split('\t')[1]

	for review in reviews:

		# added user to user set
		if review['user_id'] not in userIdDict:
			userIdDict[review['user_id']] = {'pos': 1, 'neg': 0}
		else:
			userIdDict[review['user_id']]['pos'] += 1

		f_reviews_content.write(str(cnt) + "\t" + review['review_id'] + "\t" + review['text'] + "\n")
		f_metaData.write(str(cnt) + "\t" + review['user_id'] + "\t" + businessId + "\t" + str(review['rating']) + "\t" + "-1\t" + review['date'] + "\n")

		cnt += 1

print "... finished crawling, extracted " + str(cnt-1) + " reviews in total"

cnt = 1
for userId, count in userIdDict.iteritems():
	f_userIdMapping.write(str(cnt) + "\t" + userId + "\t" + str(count['neg']) + "\t" + str(count['pos']) + "\n")
	cnt+=1


