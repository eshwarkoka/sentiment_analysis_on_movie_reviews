import os

movie_name = "baahubali"
command = "scrapy crawl imdb_spider -a ip="+movie_name+" -o result.json"

os.system(command)