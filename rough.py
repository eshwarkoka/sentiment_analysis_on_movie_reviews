from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from datetime import datetime
from time import time
import json
import os
import re
import numpy
from nltk.corpus import stopwords
from preprocess.Preprocess import PreprocessClass


#stmt = ["an apple a day keeps the", "doctor away"]

#tfidf = TfidfVectorizer(ngram_range=(1,2))

#print(tfidf.fit(stmt).vocabulary_)

# sr = "*"*40+"\n"
# #print(sr)
#
# def timing(f):
#     def wrap(*args):
#         time1 = time()
#         f(*args)
#         time2 = time()
#         #print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))
#         print(f.__name__+" function took "+str(time2-time1)[:6]+" s")
#     return wrap

# @timing
# def square(k):
#     print(k*k)
#
# square(6)

# movie_name = ["robo 1 2 3"]
# movie_name = str(movie_name[0]).replace(" ","_")
# print(movie_name)

# first_title = ['<a href="/title/tt0871510/?ref_=fn_al_tt_1">Chak de! India</a>']
# first_title = str(first_title)
# print(re.search(r'>(.+?)<',first_title).group(1))

# for each in first_title.split("/"):
#     #print(each)
#     r = re.search(r'>(.+?)<',each)
#     #if r:
#         #print(r.group(0))

# filename = "temp.txt"
# with open(filename) as f:
#     temp_str = f.read()
# print(temp_str)
# print(type(temp_str))
# os.remove(filename)

#87783

#a = numpy.arange(18).reshape(25,2)

p = PreprocessClass()


stop_words = set(stopwords.words('english'))
print(stop_words)
# with open("/Users/eshwar/Documents/projects/sentiment_analysis_on_movie_reviews/data/scraped_reviews/Arjun_Reddy.json") as f:
#     json_data = json.load(f)
# all_reviews = []
# for i in range(0, len(json_data)):
#     all_reviews.append(json_data[i]["title"] + " " + json_data[i]["review"])
# all_reviews_preprocessed = []
# for each_review in all_reviews:
#     all_reviews_preprocessed.append(p.pre_process(each_review))
# print(all_reviews_preprocessed[0])
#print(len(all_reviews_preprocessed))

#*************************


#
# import scrapy
# import json
# import re
# import requests
# from bs4 import BeautifulSoup
#
# with open('./locators/xpaths.json') as f:
#     xpaths = json.load(f)
#
# imdb = xpaths["imdb"][0]
# movie_name = ''
#
# class IMDBSpider(scrapy.Spider):
#     name = 'imdb_spider'
#     allowed_domains = ["imdb.com"]
#     start_urls = [
#         'https://www.imdb.com/find?ref_=nv_sr_fn&q='
#     ]
#
#     def start_requests(self):
#         for url in self.start_urls:
#             yield scrapy.Request(url+self.ip+"&s=all" , dont_filter=True)
#
#     def parse(self, response):
#         global movie_name
#         for url in self.start_urls:
#             imdb_content = requests.get(url+self.ip+"&s=all")
#         imdb_soup = BeautifulSoup(imdb_content.text, features='html.parser')
#         title = imdb_soup.findAll("div",class_="findSection")
#         tt = []
#         for each in title:
#             print(each.find_all('a',href=False))
#             for a in each.find_all('a',href=False):
#                 if a.has_attr("name") and a['name'].startswith("tt"):
#                     print(a["name"])
#                     print("####")
#                     print(a.contents)
#                     tt.append(each)
#             print("*****")
#         print(tt)
#         print(re.search(r'<td class="result_text">(.+?)</td>', str(tt[0])).group(1))
#         # #a_title = str(re.search(r'<a name="tt">(.+?)</td>', html_content.text).group(1))
#         #print(html_content.text[:100])
#         # data = str(html_content.text).split()
#         # for each in data:
#         #     each = each.strip()
#         #     temp = re.search(r'<a name="tt">(.*)</td>', each).group(1)
#         #     if temp:
#         #         print(temp)
#         # #get first title from all titles
#         first_title = str(response.xpath(imdb["first_title"]).extract())
#         #print(first_title)
#         #extract movie name from first title
#         movie_name = str(re.search(r'>(.+?)<',first_title).group(1)).replace(" ","_")
#         #print(movie_name)
#         title_id = ''
#         #extract title id from first title
#         for each in first_title.split("/"):
#             if each.startswith("tt"):
#                 title_id += each
#         #print(title_id)
#         #form user reviews link with title id
#         link = imdb["urv_link_part_1"]+title_id+imdb["urv_link_part_2"]
#         print(link  )
#         #scrape the link and redirect to scrape_reviews function
#         request = scrapy.Request(link, callback=self.scrape_reviews)
#         #yield request
#
#     def scrape_reviews(self, response):
#         global movie_name
#         #get authors of reviews
#         authors = response.xpath(imdb["authors"]).extract()
#         #get review dates of reviews
#         review_dates = response.xpath(imdb["review_dates"]).extract()
#         #get titles of reviews
#         titles = response.xpath(imdb["titles"]).extract()
#         titles = [title.replace("\n","") for title in titles]
#         #get ratings of reviews
#         ratings = response.xpath(imdb["ratings"]).extract()
#         del ratings[1::2]
#         #get reviews
#         reviews = response.xpath(imdb["reviews"]).extract()
#         start_review = r'<div class="text show-more__control">'
#         end_review = r'</div>'
#         reviews_list = []
#
#         for each_review in reviews:
#             temp_review = each_review[each_review.find(start_review) + len(start_review):each_review.find(end_review)]
#             temp_review = temp_review.replace("<br>", "")
#             temp_review = temp_review.replace("</br>", "")
#             reviews_list.append(temp_review)
#
#         reviews = reviews_list
#         del reviews_list
#
#         json_data = [
#             {
#                 "author" : a,
#                 "review_date" : rd,
#                 "title" : t,
#                 "rating" : ra,
#                 "review" : re
#             } for a, rd, t, ra, re in zip(authors, review_dates, titles, ratings, reviews)
#         ]
#
#         project_path = r'/Users/eshwar/Documents/projects/sentiment_analysis_on_movie_reviews/'
#         target_path = project_path+"data/scraped_reviews/"
#         output_filename = target_path+movie_name+".json"
#         with open(output_filename, 'w') as f:
#             json.dump(json_data, f, ensure_ascii=False, indent=4)
#         with open(target_path+"temp.txt", 'w') as f:
#             f.write(movie_name)