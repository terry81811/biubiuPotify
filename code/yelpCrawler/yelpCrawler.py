from random import *
from time import sleep
import io, time, json
from collections import OrderedDict
from operator import itemgetter

from yelpAPI import *

__author__ = 'Terry Tsai'



# return rows of (userId, neg, pos)
def getSuspiciousUsers(inputFile, outputFile):
	print ">>> in getSuspiciousUsers"

	f_in = open('outputData_Final/' + inputFile + '.tsv', 'r')
	userParts = [line.rstrip('\n\r').split("\t") for line in f_in]

	f_out = open('outputData_Final/' + outputFile + '.tsv', 'w')
	for userPart in userParts:
		if int(userPart[2]) + int(userPart[3]) > 1 and int(userPart[3]) > 0:
			f_out.write("\t".join(userPart) + "\n")



# return rows of (reviewId, userId, businessId)
def crawlUserReviews(inputFile, outputFile1, outputFile2, start):
	print ">>> in crawlUserReviews"

	f_in = open('outputData_Final/' + inputFile + '.tsv', 'r')
	userParts = [line.rstrip('\n\r').split("\t") for line in f_in]


	print ">>> preparing to read " + str(len(userParts)) + " user reviews"

	# sleep for 2 minute between every 100 users
	for offsetIndex in range(start, len(userParts) / 100 + 1):
		offset = offsetIndex * 100
		# print offsetIndex
		f_out_meta = io.open('outputData_Final/suspiciousReviewerReviews/' + outputFile1 + "_" + str(offset) + '.tsv', 'w', encoding='utf8')
		f_out_content = io.open('outputData_Final/suspiciousReviewerReviews/' + outputFile2 + "_" + str(offset) + '.tsv', 'w', encoding='utf8')

		cnt = 1
		for part in userParts[offset: offset + 100]:
			reviews = getReviewFromUserPage(part[1])
			print ">>> " + part[0] + "  extracted " + str(len(reviews)) + " from user: " + part[1]

			for review in reviews:

				f_out_meta.write(str(cnt) + "\t" + review['reviewId'] + "\t" + part[1] + "\t" + review['bizId'] + "\n")
				f_out_content.write(str(cnt) + "\t" + review['reviewId'] + "\t" + review['reviewContent'] + "\n")

				cnt += 1

		f_out_meta.close()
		f_out_content.close()

		print ">>> file: " + str(offset) + " is written. sleep for 2 minutes..."
		sleep(120)




# return rows of (userId, # of reviews)
def crawUserReviewMetaData(userList, outputFile):
	print ">>> in crawUserReviewMetaData"
	pass




# second order function
def combineBizFromReviews(inputFiles, outputFile):
	print ">>> in combineBizFromReviews"

	l = []
	bizList = OrderedDict()
	f_out_meta = open('outputData_Final/' + outputFile + '.tsv', 'w')

	for i in range(25):
		f_in = open('outputData_Final/suspiciousReviewerReviews/' + inputFiles + "_" + str(i*100) + '.tsv', 'r')
		reviewParts = [line.rstrip('\n\r').split("\t") for line in f_in]

		for review in reviewParts:
			l.append(review)
			bizList[review[3]] = True

	cnt = 1
	for k, v in bizList.iteritems():
		f_out_meta.write(str(cnt) + "\t" + k + "\n")
		cnt += 1


def crawlBizReviews(inputFile, outputFile1, outputFile2, start):
	print ">>> in crawlBizReviews / reviewsOfBizReviewedBySuspiciousReviewer"

	f_in = open('outputData_Final/' + inputFile + '.tsv', 'r')
	businessParts = [line.rstrip('\n\r').split("\t") for line in f_in]

	print ">>> preparing to crawl " + str(len(businessParts)) + " businesses reviews"

	# sleep for 2 minute between every 100 users
	for offsetIndex in range(start, len(businessParts) / 100 + 1):
		offset = offsetIndex * 100
		f_out_meta = io.open('outputData_Final/reviewsOfBizReviewedBySuspiciousReviewer/' + outputFile1 + "_" + str(offset) + '.tsv', 'w', encoding='utf8')
		f_out_content = io.open('outputData_Final/reviewsOfBizReviewedBySuspiciousReviewer/' + outputFile2 + "_" + str(offset) + '.tsv', 'w', encoding='utf8')

		cnt = 1
		for part in businessParts[offset: offset + 100]:

			print ">>> " + part[0] + " extracting recommended reviews from: " + part[1]
			url = 'https://www.yelp.com/biz/' + part[1]
			# print url
			reviews = extract_reviews(url)
			print ">>> extrated " + str(len(reviews)) + " from " + part[1]

			for review in reviews:
				f_out_content.write(str(cnt) + "\t" + review['review_id'] + "\t" + review['text'] + "\n")
				f_out_meta.write(str(cnt) + "\t" + review['user_id'] + "\t" + part[0] + "\t" + str(review['rating']) + "\t" + "1\t" + review['date'] + "\n")
				cnt += 1

			print ">>> " + part[0] + "  extracting non-recommended reviews from: " + part[1]
			url = '/not_recommended_reviews/' + part[1]
			reviews = extract_unrecommend_reviews(url)
			print ">>> extrated " + str(len(reviews)) + " from " + part[1]

			for review in reviews:

				f_out_content.write(str(cnt) + "\t" + review['review_id'] + "\t" + review['text'] + "\n")
				f_out_meta.write(str(cnt) + "\t" + review['user_id'] + "\t" + part[0] + "\t" + str(review['rating']) + "\t" + "-1\t" + review['date'] + "\n")
				cnt += 1


		f_out_meta.close()
		f_out_content.close()

		print ">>> file: " + str(offset) + " is written. sleep for 2 minutes..."
		sleep(120)	


# return row of (businessId, # of recommend reviews, # of not recommend reviews)
def crawBusinessMetaData(inputFile, outputFile, start, term):
	print ">>> in crawBusinessMetaData"

	f_in = io.open('outputData_Final/' + inputFile + '_' + term + '.tsv', 'r', encoding="utf8")
	businesses = [line.rstrip('\n\r').split("\t")[1] for line in f_in]

	f_out_meta = io.open('outputData_Final/' + outputFile + '_' + term + '_' + str(start) +'.tsv', 'w', encoding='utf8')


	for biz in businesses[start: -1]:
		print ">>> extracting meta for biz: " + biz
		meta = getMetaDataFromBiz(biz)
		print meta
		f_out_meta.write(biz + "\t" + "\t".join(meta) + "\n")


def rankTopSuspiciousBiz(inputFile, outputFile):
	print ">>> rankTopSuspiciousBiz"

	f_in = io.open('outputData_Final/' + inputFile + '.tsv', 'r', encoding="utf8")
	businessesParts = [line.rstrip('\n\r').split("\t") for line in f_in]

	f_out_meta = io.open('outputData_Final/' + outputFile +'.tsv', 'w', encoding='utf8')

	rank = []
	bizDict = {}

	for biz in businessesParts:
		rank.append((biz[0], float(biz[2]) / (float(biz[2]) + float(biz[3]))))
		bizDict[biz[0]] = biz

	sortedRank = sorted(rank, key=itemgetter(1))

	for item in sortedRank:
		f_out_meta.write(item[0] + "\t" + str(item[1]) + "\t" + bizDict[item[0]][1] + "\t" + bizDict[item[0]][2] + "\t" + bizDict[item[0]][3] + "\n")


# def crawBusinessMetaDataByLocation(term, start):
	
# 	# load 1000 restaurants 
# 	client = authenticate("inputData/authenticate.json")
# 	businesses = all_restaurants(client, term)

# 	print ">>> get restaurants count in " + term + " : " + str(len(businesses))

# 	cnt = 1
# 	f = io.open('outputData_Final/businessesIdMapping_' + start + '.tsv', 'w', encoding='utf8')
# 	for business in businesses:
# 		f.write(str(cnt) + "\t" + business.id + "\n")
# 		cnt += 1	

# 	crawBusinessMetaData('businessesIdMapping_' + term, 'businesses_meta_data_' + term)


# getSuspiciousUsers('user_id_mapping_All', 'suspicious_user_id_mapping')

# crawlUserReviews('suspicious_user_id_mapping', 'suspicious_user_reviews_meta', 'suspicious_user_reviews_content', 6)

# crawlBizReviews('suspicious_user_reviewed_biz', 'suspicious_user_reviews_meta', 'suspicious_user_reviews_content', 0)

# reviews = extract_reviews('https://www.yelp.com/biz/butcher-and-the-rye-pittsburgh')

crawBusinessMetaData('businessesIdMapping', 'businesses_meta_data', 500, 'San Jose')

# rankTopSuspiciousBiz('businesses_meta_data_Pittsburgh', 'top_suspicious_biz_Pittsburgh')

# crawBusinessMetaDataByLocation('Pittsburgh', 850)



