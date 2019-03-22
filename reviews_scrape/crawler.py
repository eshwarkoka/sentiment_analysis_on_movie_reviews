import os

movie_name = "dangal"
command = "scrapy crawl imdb_spider -a ip="+movie_name

os.system(command)