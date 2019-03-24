from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from datetime import datetime
import time

#stmt = ["an apple a day keeps the", "doctor away"]

#tfidf = TfidfVectorizer(ngram_range=(1,2))

#print(tfidf.fit(stmt).vocabulary_)

sr = "*"*40+"\n"
#print(sr)

def timing(f):
    def wrap(*args):
        time1 = time.time()
        f(*args)
        time2 = time.time()
        #print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))
        print(f.__name__+" function took "+str((time2-time1)*1000)[:6]+" ms")
    return wrap

@timing
def square(k):
    print(k*k)

square(6)




