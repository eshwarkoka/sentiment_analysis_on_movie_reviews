import os,sys,json
from preprocess_reviews.Preprocess import Preprocess

p = Preprocess()


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

movie_name = "raatsasan"
movie_name = movie_name.replace(" ","")
execute_crawler(movie_name)
preprocess(movie_name)
#def preprocess:

#with open('./reviews_scrape/target/bahubali.json') as f:
#    reviews = json.load(f)

#print(reviews[1]["review"])