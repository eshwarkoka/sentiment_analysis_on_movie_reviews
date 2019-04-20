import os, json, collections, nltk, glob
from nltk.util import ngrams
from preprocess.Preprocess import PreprocessClass
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

#create the instance of PreprocessClass
p = PreprocessClass()

#define all the required variables
project_path = "/Users/eshwar/Documents/projects/sentiment_analysis_on_movie_reviews/"
data_path = project_path+"data/"
predicted_reviews_path = data_path+"predicted_reviews/"
scraped_reviews_path = data_path+"scraped_reviews/"
preprocessed_dataset_path = project_path+'data/dataset_preprocessed/'
preprocessed_train_path = preprocessed_dataset_path+"full_train_preprocessed.txt"
preprocessed_test_path = preprocessed_dataset_path+"full_test_preprocessed.txt"
movie_file_name = ''

#create target/class-label list for the dataset
target = []
for i in range(0,50000):
    if 0 < i < 12500 or 25000 < i < 37500:
        target.append(1)
    else:
        target.append(0)

#get all the preprocessed train test reviews
dataset_reviews = []
for line in open(preprocessed_train_path,'r'):
    review = line.strip()
    dataset_reviews.append(review)

for line in open(preprocessed_test_path,'r'):
    review = line.strip()
    dataset_reviews.append(review)

#function which gets the movie name stored in temp.txt file
def get_movie_file_name():
    global movie_file_name
    temp_file_name = scraped_reviews_path+"temp.txt"
    with open(temp_file_name) as f:
        movie_file_name = f.read()
    os.remove(temp_file_name)

#function which execute the crawler provided movie name
def execute_crawler(movie_name):
    current_dir = os.getcwd()
    change_dir = current_dir + '/scrape_reviews'
    os.chdir(change_dir)
    os.system("python crawler.py " + movie_name)
    get_movie_file_name()
    os.chdir(current_dir)
    try:
        with open(project_path+"flag.txt") as f:
            flag = f.read()
        if flag == "0":
            os.remove(project_path+"flag.txt")
            print_score(movie_file_name)
    except IOError:
        preprocess_scraped_reviews()

#function which preprocesses the scraped reviews
def preprocess_scraped_reviews():
    global movie_file_name
    review_path = scraped_reviews_path+movie_file_name+".json"
    with open(review_path) as f:
        json_data = json.load(f)
    all_reviews = []
    for i in range(0,len(json_data)):
        all_reviews.append(json_data[i]["title"]+" "+json_data[i]["review"])
    all_reviews_preprocessed = []
    for each_review in all_reviews:
        all_reviews_preprocessed.append(p.pre_process(each_review))
    print(len(all_reviews_preprocessed))
    #most_common_words(all_reviews_preprocessed)
    feed_reviews_to_classifier(all_reviews_preprocessed)

def most_common_words(list):
    tokens = []
    for each_list in list:
        tokens.extend(nltk.word_tokenize(each_list))
    unigrams = ngrams(tokens, 1)
    counter = collections.Counter(unigrams)
    print(counter.most_common(20))
    print("*******")
    bigrams = ngrams(tokens, 2)
    counter = collections.Counter(bigrams)
    print(counter.most_common(20))

def feed_reviews_to_classifier(preprocessed_reviews):
    tfidf = TfidfVectorizer()
    X = tfidf.fit_transform(dataset_reviews)
    print(X.shape)
    X_test = tfidf.transform(preprocessed_reviews)
    print(X_test.shape)
    svm = LinearSVC()
    svm.fit(X, target)
    predicted = svm.predict(X_test)
    generate_score(predicted)

def generate_score(predicted):
    predicted_len = len(predicted)
    print("Number of reviews scraped: " + str(predicted_len))
    pos_rev_len = len([i for i in predicted if i])
    print("Number of positive reviews: " + str(pos_rev_len))
    neg_rev_len = len([i for i in predicted if not i])
    print("Number of negative reviews: " + str(neg_rev_len))
    overall_score = str((pos_rev_len/predicted_len)*100)
    print("Overall score: " + overall_score)

    #store the output
    json_data = [
        {
            "reviews_scraped"  : str(predicted_len),
            "positive_reviews" : str(pos_rev_len),
            "negative_reviews" : str(neg_rev_len),
            "overall_score"    : overall_score
        }
    ]
    with open(predicted_reviews_path+movie_file_name+".json", "w") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

def print_score(movie_name):
    temp_name = movie_name.split("$#$")[0]+"$#$"
    os.chdir(predicted_reviews_path)
    file_name = glob.glob(temp_name+"*")
    with open(predicted_reviews_path+file_name[0]) as f:
        json_data = json.load(f)
    print("Reviews scraped : " + json_data[0]["reviews_scraped"])
    print("Positive reviews : " + json_data[0]["positive_reviews"])
    print("Negative reviews : " + json_data[0]["negative_reviews"])
    print("Overall score : " + json_data[0]["overall_score"])


#main code which executes only when this file is executed
if __name__ == "__main__":
    movie_name = "arjun reddy"
    movie_name = movie_name.replace(" ","")
    execute_crawler(movie_name)
    print("**DONE**")
