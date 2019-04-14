import os,sys

movie_name = sys.argv[1]

command = "scrapy crawl imdb_spider_2 -a ip="+movie_name

os.system(command)
#print(command)