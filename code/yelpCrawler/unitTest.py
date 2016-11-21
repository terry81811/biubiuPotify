from yelpAPI import *

# function unit test of yelpAPI functions


# html = retrieve_html('https://www.yelp.com/biz/t%C3%A4k%C5%8D-pittsburgh')
# res = parse_page(html[1])
# print len(res[0])
# print res[1]


# # test bad reviews

# html = retrieve_html('https://www.yelp.com/not_recommended_reviews/t%C3%A4k%C5%8D-pittsburgh')
# res = parse_page_not_recommend(html[1])
# print len(res[0])
# print res[1]

# res = extract_reviews('https://www.yelp.com/biz/t%C3%A4k%C5%8D-pittsburgh')
# print len(res)

# res = extract_unrecommend_reviews('/not_recommended_reviews/t%C3%A4k%C5%8D-pittsburgh')
# print len(res)

# res = extract_reviews('https://www.yelp.com/biz/streets-on-carson-pittsburgh')
# print len(res)

# res = extract_unrecommend_reviews('/not_recommended_reviews/streets-on-carson-pittsburgh')
# print len(res)

# res = extract_reviews('https://www.yelp.com/biz/gaucho-parrilla-argentina-pittsburgh')
# print len(res)

# res = extract_unrecommend_reviews('/not_recommended_reviews/gaucho-parrilla-argentina-pittsburgh')
# print len(res)

# res = extract_reviews('https://www.yelp.com/biz/bigham-tavern-pittsburgh')
# print len(res)

# res = extract_unrecommend_reviews('/not_recommended_reviews/bigham-tavern-pittsburgh')
# print len(res)


res = extract_reviews('https://www.yelp.com/biz/tessaros-pittsburgh-2')
print len(res)

res = extract_unrecommend_reviews('/not_recommended_reviews/tessaros-pittsburgh-2')
print len(res)

res = extract_reviews('https://www.yelp.com/biz/nickys-thai-kitchen-pittsburgh-4')
print len(res)

res = extract_unrecommend_reviews('/not_recommended_reviews/nickys-thai-kitchen-pittsburgh-4')
print len(res)
