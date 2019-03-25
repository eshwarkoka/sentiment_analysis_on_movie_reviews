import os,sys,json,glob
from preprocess.Preprocess import PreprocessClass

p = PreprocessClass()

project_path = "/Users/eshwar/Documents/projects/sentiment_analysis_on_movie_reviews/"
scraped_reviews_path = project_path+"data/scraped_reviews/"

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
    authors = []
    for i in range(0,len(json_data)):
        authors.append(json_data[i]["author"])
    print(authors)

movie_name = "tanioruvan"
movie_name = movie_name.replace(" ","")
execute_crawler(movie_name)

