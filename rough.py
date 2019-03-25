from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from datetime import datetime
from time import time
import os
import re

#stmt = ["an apple a day keeps the", "doctor away"]

#tfidf = TfidfVectorizer(ngram_range=(1,2))

#print(tfidf.fit(stmt).vocabulary_)

sr = "*"*40+"\n"
#print(sr)

def timing(f):
    def wrap(*args):
        time1 = time()
        f(*args)
        time2 = time()
        #print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))
        print(f.__name__+" function took "+str(time2-time1)[:6]+" s")
    return wrap

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

filename = "temp.txt"
with open(filename) as f:
    temp_str = f.read()
print(temp_str)
print(type(temp_str))
os.remove(filename)