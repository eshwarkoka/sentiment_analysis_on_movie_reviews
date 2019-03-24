from preprocess.Preprocess import PreprocessClass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
import time

p = PreprocessClass()

#get all the train and test reviews from preprocessed dataset
preprocessed_dataset_path = r'/Users/eshwar/Documents/projects/sentiment_analysis_on_movie_reviews/data/dataset_preprocessed/'
preprocessed_train_path = preprocessed_dataset_path+"full_train_preprocessed.txt"
preprocessed_test_path = preprocessed_dataset_path+"full_test_preprocessed.txt"

all_reviews = []

for line in open(preprocessed_train_path,'r'):
    review = line.strip()
    all_reviews.append(review)

for line in open(preprocessed_test_path,'r'):
    review = line.strip()
    all_reviews.append(review)

target = []
for i in range(0,50000):
    if 0 < i < 12500 or 25000 < i < 37500:
        target.append(1)
    else:
        target.append(0)

starline = "\n"+"*"*50+"\n"
output_file_str = ""
output_file_str += starline

def timer(func):
    def wrapper(*args,**kwargs):
        global output_file_str
        time1 = time.time()
        func(*args,**kwargs)
        time2 = time.time()
        output_file_str += func.__name__+" function took "+str((time2-time1)/60)[:6]+" min"+starline
    return wrapper

@timer
def logistic_regression(trainsize=0.5, ng_min=1, ng_max=1):
    global output_file_str
    output_file_str += "Logistic Regression:\nTrain size = "+str(trainsize)+"\nn-grams=("+str(ng_min)+","+str(ng_max)+")\n"
    tfidf = TfidfVectorizer(ngram_range=(ng_min, ng_max))
    X = tfidf.fit_transform(all_reviews)
    X_train, X_test, y_train, y_test = train_test_split(X, target, train_size=trainsize)
    lr = LogisticRegression(solver='lbfgs')
    lr.fit(X_train, y_train)
    acc_score = accuracy_score(y_test, lr.predict(X_test))
    output_file_str += "Accuracy Score: "+str(acc_score)+"\n"

@timer
def linear_svc(trainsize=0.5, ng_min=1, ng_max=1):
    global output_file_str
    output_file_str += "Support Vector Machine:\nTrain size = "+str(trainsize)+"\nn-grams=("+str(ng_min)+","+str(ng_max)+")\n"
    tfidf = TfidfVectorizer(ngram_range=(ng_min, ng_max))
    X = tfidf.fit_transform(all_reviews)
    X_train, X_test, y_train, y_test = train_test_split(X, target, train_size=trainsize)
    svm = LinearSVC()
    svm.fit(X_train, y_train)
    acc_score = accuracy_score(y_test, svm.predict(X_test))
    output_file_str += "Accuracy Score: " +str(acc_score)+ "\n"

@timer
def decision_tree(trainsize=0.5, ng_min=1, ng_max=1):
    global output_file_str
    output_file_str += "Decison Tree:\nTrain size = "+str(trainsize)+"\nn-grams=("+str(ng_min)+","+str(ng_max)+")\n"
    tfidf = TfidfVectorizer(ngram_range=(ng_min, ng_max))
    X = tfidf.fit_transform(all_reviews)
    X_train, X_test, y_train, y_test = train_test_split(X, target, train_size=trainsize)
    dt = DecisionTreeClassifier()
    dt.fit(X_train, y_train)
    acc_score = accuracy_score(y_test, dt.predict(X_test))
    output_file_str += "Accuracy Score: " +str(acc_score)+ "\n"

if __name__ == '__main__':

    #logistic regression
    #train_size = 0.5, ng_max = 1
    logistic_regression(trainsize=0.5, ng_max=1)
    print("lr1 completed")
    #train_size = 0.5, ng_max = 2
    logistic_regression(trainsize=0.5, ng_max=2)
    print("lr2 completed")
    # train_size = 0.75, ng_max = 1
    logistic_regression(trainsize=0.75, ng_max=1)
    print("lr3 completed")
    # train_size = 0.75, ng_max = 2
    logistic_regression(trainsize=0.75, ng_max=2)
    print("lr4 completed")

    # support vector machine
    # train_size = 0.5, ng_max = 1
    linear_svc(trainsize=0.5, ng_max=1)
    print("svm1 completed")
    # train_size = 0.5, ng_max = 2
    linear_svc(trainsize=0.5, ng_max=2)
    print("svm2 completed")
    # train_size = 0.75, ng_max = 1
    linear_svc(trainsize=0.75, ng_max=1)
    print("svm3 completed")
    # train_size = 0.75, ng_max = 2
    linear_svc(trainsize=0.75, ng_max=2)
    print("svm4 completed")

    # decision tree
    # train_size = 0.5, ng_max = 1
    decision_tree(trainsize=0.5, ng_max=1)
    print("dt1 completed")
    # train_size = 0.5, ng_max = 2
    #decision_tree(trainsize=0.5, ng_max=2)
    #print("dt2 completed")
    # train_size = 0.75, ng_max = 1
    decision_tree(trainsize=0.75, ng_max=1)
    print("dt3 completed")
    # train_size = 0.75, ng_max = 2
    #decision_tree(trainsize=0.75, ng_max=2)
    #print("dt4 completed")

    with open("classifiers_comparision_output.txt", "w") as output_file:
        output_file.write(output_file_str)
    print("**DONE**")

