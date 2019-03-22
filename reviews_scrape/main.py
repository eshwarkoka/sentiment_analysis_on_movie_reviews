import os

movie_name = "inception"
command = "scrapy crawl imdb_spider -a ip="+movie_name

os.system(command)