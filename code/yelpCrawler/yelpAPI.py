# setup library imports
import io, time, json
import re
import requests
from bs4 import BeautifulSoup
import traceback

import random
from time import sleep

# import yelp client library
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

def authenticate(config_filepath):

	with io.open(config_filepath) as cred:
		creds = json.load(cred)
		auth = Oauth1Authenticator(**creds)
		client = Client(auth)

	return client

def retrieve_html(url):
	with requests.Session() as s:
		r = s.get(url, auth=('user', 'pass'))
		return (r.status_code, r.text)

def getReviews(userId): 
	print ">>> in getReviews of user: " + userId
	url = "https://www.yelp.com/user_details_reviews_self?userid=" + userId
	t = retrieve_html(url)
	soup = BeautifulSoup(t[1], 'html.parser')

	errorPageDiv = soup.find_all('body', class_="error-page")

	return len(errorPageDiv) == 0


def all_restaurants(client, query):

	print ">>> in all_restaurants"

	offset = 0
	newL = list()
	params = {
		'category_filter': 'restaurants',
		'offset': offset,
	}

	res = client.search(query, **params)
	total = res.total

	while (offset < total) and (offset < 1000):
		params['offset'] = offset
		res = client.search(query, **params)
		newL.extend(res.businesses)
		offset += 20
		# print offset

	return newL


# Q3
def parse_page(html):

	soup = BeautifulSoup(html, 'html.parser')

	# find reviews
	l = list()

	try:
		recommend_review_container = soup.find('div', class_="review-list")
		reviews = recommend_review_container.find_all('div', class_="review review--with-sidebar")

		for r in reviews:
			try:
				review_id = r.get('data-review-id')

				user_photo = r.find('a', class_="user-photo js-analytics-click")
				user_id = r.get('data-signup-object').split(":")[1]
				rating = r.find('div', class_="rating-very-large").get('title').split(" ")[0]
				date = re.sub(r"\s+", '', r.find('span', class_="rating-qualifier").get_text())
				text = r.find('div', class_="review-content").find('p').get_text()

				l.append({
					'review_id': review_id,
					'user_id': user_id,
					'rating': float(rating),
					'date': date,
					'text': text,		   
					})
			except:
				print ">>> EXCEPTION: a review can not be extract. Ignore"
				traceback.print_exc()
				pass
	except:
		print ">>> EXCEPTION: reviews can not be extract. Ignore"
		traceback.print_exc()
		pass


	# find next page
	next = soup.find_all('a', class_="u-decoration-none next pagination-links_anchor")

	if len(next) != 0:
		nextLink = next[0].get('href')
	else:
		nextLink = ""

	return (l, nextLink)




# Q4 for not-recommended reviews:
def parse_page_not_recommend(html):

	soup = BeautifulSoup(html, 'html.parser')

	# find reviews
	l = list()

	try:
		not_recommended_reviews = soup.find('div', class_='not-recommended-reviews')
		reviews = not_recommended_reviews.find_all('div', class_="review review--with-sidebar")

		for r in reviews:
			try:
				review_id = r.get('data-review-id')
				user_id = r.get('data-signup-object').split(":")[1]
				rating = r.find('div', class_="rating-very-large").get('title').split(" ")[0]
				date = re.sub(r"\s+", '', r.find('span', class_="rating-qualifier").get_text())
				text = r.find('div', class_="review-content").find('p').get_text()

				l.append({
					'review_id': review_id,
					'user_id': user_id,
					'rating': float(rating),
					'date': date,
					'text': text,		   
					})
			except:
				print ">>> EXCEPTION: a review can not be extract. Ignore"
				pass
	except:
		print ">>> EXCEPTION: reviews can not be extract. Ignore"
		traceback.print_exc()
		pass

	# find next page
	pagination = soup.find('div', 'pagination-links arrange_unit')
	nextLink = ""
	if pagination is not None:
		next = pagination.find_all('a', class_="u-decoration-none next pagination-links_anchor")
		if len(next) != 0:
			nextLink = next[0].get('href')

	return (l, nextLink)


def extract_reviews(url):
	
	pl = list()
	pUrl = url

	while pUrl != "":
		# sleep(random.random() * 2)

		html = retrieve_html(pUrl)[1]
		pRes = parse_page(html)

		pl.extend(pRes[0])
		pUrl = pRes[1]

	return pl


def extract_unrecommend_reviews(url):
	nl = list()
	nUrl = url

	while nUrl != "":
		# sleep(random.random() * 2)

		html = retrieve_html('https://www.yelp.com' + nUrl)[1]
		nRes = parse_page_not_recommend(html)

		nl.extend(nRes[0])
		nUrl = nRes[1]

	return nl


def parseUserPage(html):
	soup = BeautifulSoup(html, 'html.parser')

	# find reviews
	l = list()

	try:
		# not_recommended_reviews = soup.find('div', class_='not-recommended-reviews')
		businesses = soup.find_all('a', class_="biz-name js-analytics-click")

		# get business 
		for b in businesses:
			l.append(b.get('href').split("/")[2])


		# find next page
		pagination = soup.find('div', 'pagination-links arrange_unit')
		nextLink = ""
		if pagination is not None:
			next = pagination.find_all('a', class_="u-decoration-none next pagination-links_anchor")
			if len(next) != 0:
				nextLink = next[0].get('href')

		# print nextLink
		# print l
		return (l, nextLink)

	except:
		print ">>> EXCEPTION: reviews can not be extract. Ignore"
		traceback.print_exc()
		pass

def getBizFromUserPage(userId):

	bizList = list()
	url = 'https://www.yelp.com/user_details_reviews_self?userid=' + userId + '&rec_pagestart=0'

	while url != "":
		html = retrieve_html(url)[1]
		res = parseUserPage(html)

		bizList.extend(res[0])
		url = res[1]


	return bizList


def parseUserReviews(html):
	soup = BeautifulSoup(html, 'html.parser')

	# find reviews
	l = list()

	try:
		# not_recommended_reviews = soup.find('div', class_='not-recommended-reviews')
		# businesses = soup.find_all('a', class_="biz-name js-analytics-click")

		reviewContainer = soup.find('div', class_='user-details_reviews')
		reviews = reviewContainer.find_all('div', class_="review")

		for r in reviews:
			try:
				reviewId = r.get('data-review-id')
				bizId = r.find('a', class_="biz-name js-analytics-click").get('href').split("/")[2]
				reviewContent = r.find('div', class_="review-content").find('p').get_text()

				l.append({
					'reviewId': reviewId,
					'bizId': bizId,
					'reviewContent': reviewContent,		   
					})
			except:
				print ">>> EXCEPTION: a review can not be extract. Ignore"
				pass


		# find next page
		pagination = soup.find('div', 'pagination-links arrange_unit')
		nextLink = ""
		if pagination is not None:
			next = pagination.find_all('a', class_="u-decoration-none next pagination-links_anchor")
			if len(next) != 0:
				nextLink = next[0].get('href')

		return (l, nextLink)

	except:
		print ">>> EXCEPTION: reviews can not be extract. Ignore"
		traceback.print_exc()
		return (l, "")
		pass



def getReviewFromUserPage(userId):

	reviewList = list()
	url = 'https://www.yelp.com/user_details_reviews_self?userid=' + userId + '&rec_pagestart=0'

	while url != "":
		html = retrieve_html(url)[1]
		res = parseUserReviews(html)

		reviewList.extend(res[0])
		url = res[1]

	return reviewList


def getMetaDataFromBiz(bizId):

	url = "https://www.yelp.com/biz/" + bizId
	html = retrieve_html(url)[1]
	soup = BeautifulSoup(html, 'html.parser')
	infoContainer = soup.find('div', class_='biz-main-info embossed-text-white')
	stars = infoContainer.find('div', class_='rating-very-large').get('title').split(" ")[0]
	recommendCountText = infoContainer.find('span', 'review-count rating-qualifier').get_text()
	recommendCount = ' '.join(recommendCountText.split()).split(" ")[0]

	try:
		notRecommendedContainer = soup.find('div', class_= 'not-recommended ysection')
		notRecommendCountText = notRecommendedContainer.find('a', class_='subtle-text').get_text()
		notRecommendCount = ' '.join(notRecommendCountText.split()).split(" ")[0]

	except:
		print ">>> EXCEPTION: could not find notRecommend Count. return 0"
		notRecommendCount = '0'

	url = "https://www.yelp.com/not_recommended_reviews/" + bizId

	return [stars, recommendCount, notRecommendCount]