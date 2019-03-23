import os,sys,json
import numpy as np
from preprocess_reviews.Preprocess import Preprocess
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC

p = Preprocess()

reviews = []
for line in open('full_train.txt','r'):
    temp = line.strip()
    temp_str = p.pre_process(temp)
    reviews.append(temp_str)
print(len(reviews))

for line in open('full_test.txt','r'):
    temp = line.strip()
    temp_str = p.pre_process(temp)
    reviews.append(temp_str)
print(len(reviews))

tfidf_vectorizer = TfidfVectorizer(ngram_range=(1,2))
X = tfidf_vectorizer.fit_transform(reviews)


print(X.shape)

target = []
for i in range(0,50000):
    if 0 < i < 12500 or 25000 < i < 37500:
        target.append(1)
    else:
        target.append(0)

#target = [1 if i < 12500 else 0 for i in range(25000)]

X_train, X_test, y_train, y_test = train_test_split(
     X, target, train_size = 0.5
)

print(X_train.shape)
print(X_test.shape)

# for c in [0.01, 0.05, 0.25, 0.5, 1]:
#     lr = LogisticRegression(C=c,solver='lbfgs')
#     lr.fit(X_train, y_train)
#     print(lr.predict(X_test))
#     print("Accuracy for C=%s: %s"
#           % (c, accuracy_score(y_test, lr.predict(X_test))))

# dt = DecisionTreeClassifier()
# dt.fit(X_train, y_train)
# predicted_dt = dt.predict(X_test)
# print(predicted_dt)
# score_dt=np.mean(predicted_dt == y_test)
# print('score of DT: '+str(score_dt))

for c in [0.01, 0.05, 0.25, 0.5, 1]:
    svm = LinearSVC(C=c)
    svm.fit(X_train, y_train)
    print("SVM Accuracy for C=%s: %s"
          % (c, accuracy_score(y_test, svm.predict(X_test))))

def execute_crawler(movie_name):
    current_dir = os.getcwd()
    change_dir = current_dir + '/reviews_scrape'
    os.chdir(change_dir)
    os.system("python crawler.py " + movie_name)

def preprocess(movie_name):
    json_target_path = "./target/"+movie_name+".json"
    print(os.getcwd())
    with open(json_target_path) as f:
        json_data = json.load(f)
    authors = []
    for i in range(0,len(json_data)):
        authors.append(json_data[i]["author"])
    print(authors)

#movie_name = "raatsasan"
#movie_name = movie_name.replace(" ","")
#execute_crawler(movie_name)
#preprocess(movie_name)
#def preprocess:

