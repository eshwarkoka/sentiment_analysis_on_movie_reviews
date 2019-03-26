import os,json
import pickle
from preprocess.Preprocess import PreprocessClass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.externals import joblib

p = PreprocessClass()

project_path = "/Users/eshwar/Documents/projects/sentiment_analysis_on_movie_reviews/"
scraped_reviews_path = project_path+"data/scraped_reviews/"
preprocessed_dataset_path = project_path+'data/dataset_preprocessed/'
preprocessed_train_path = preprocessed_dataset_path+"full_train_preprocessed.txt"
preprocessed_test_path = preprocessed_dataset_path+"full_test_preprocessed.txt"

target = []
for i in range(0,50000):
    if 0 < i < 12500 or 25000 < i < 37500:
        target.append(1)
    else:
        target.append(0)

dataset_reviews = []

for line in open(preprocessed_train_path,'r'):
    review = line.strip()
    dataset_reviews.append(review)

for line in open(preprocessed_test_path,'r'):
    review = line.strip()
    dataset_reviews.append(review)

# def generate_svm_train_pickle():
#     tfidf_vectorizer = TfidfVectorizer()
#     tfidf_vectorizer.fit_transform(dataset_reviews)
#     #svm = LinearSVC()
#     #svm.fit(X, target)
#     with open("svm_train.pickle", "wb") as f:
#         pickle.dump(tfidf_vectorizer, f)
#     print("svm pickle generated !!")

def execute_crawler(movie_name):
    current_dir = os.getcwd()
    change_dir = current_dir + '/reviews_scrape'
    os.chdir(change_dir)
    os.system("python crawler.py " + movie_name)
    preprocess_scraped_reviews()

def preprocess_scraped_reviews():
    temp_file_name = scraped_reviews_path+"temp.txt"
    with open(temp_file_name) as f:
        temp_str = f.read()
    movie_name = temp_str
    os.remove(temp_file_name)
    review_path = scraped_reviews_path+movie_name+".json"
    with open(review_path) as f:
        json_data = json.load(f)
    all_reviews = []
    for i in range(0,len(json_data)):
        all_reviews.append(json_data[i]["title"]+" "+json_data[i]["review"])
    all_reviews_preprocessed = []
    for each_review in all_reviews:
        all_reviews_preprocessed.append(p.pre_process(each_review))
    print(len(all_reviews_preprocessed))
    feed_reviews_to_classifier(all_reviews_preprocessed)

def feed_reviews_to_classifier(preprocessed_reviews):
    tfidf = TfidfVectorizer()
    X = tfidf.fit_transform(dataset_reviews)
    print(X.shape)
    X_test = tfidf.transform(preprocessed_reviews)
    print(X_test.shape)
    svm = LinearSVC()
    svm.fit(X, target)
    print(svm.predict(X_test))

# generate_svm_train_pickle()

movie_name = "billa"
movie_name = movie_name.replace(" ","")
execute_crawler(movie_name)
print("**DONE**")
