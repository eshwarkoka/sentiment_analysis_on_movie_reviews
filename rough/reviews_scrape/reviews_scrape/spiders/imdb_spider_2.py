import scrapy
import json
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

with open('./locators/xpaths.json') as f:
    xpaths = json.load(f)

imdb = xpaths["imdb"][0]
movie_name = ''
link = ''
#chrome_driver = webdriver.Chrome('/Users/eshwar/Documents/projects/sentiment_analysis_on_movie_reviews/reviews_scrape/reviews_scrape/spiders/chromedriver')

class IMDBSpider(scrapy.Spider):
    name = 'imdb_spider_2'
    allowed_domains = ["imdb.com"]
    start_urls = [
        'https://www.imdb.com/find?ref_=nv_sr_fn&q='
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url+self.ip+"&s=tt" , dont_filter=True)

    def parse(self, response):
        global movie_name
        global link
        first_title = response.xpath(imdb["first_title"]).extract()
        print(first_title)

        # for url in self.start_urls:
        #     imdb_content = requests.get(url+self.ip+"&s=all")
        # imdb_soup = BeautifulSoup(imdb_content.text, features='html.parser')
        # #get all tables
        # tables = imdb_soup.findAll("div",class_="findSection")
        # #get tables which contains <a name="tt> </aa> because we want Titles, not Names
        # tt = ""
        # for each_table in tables:
        #     for a in each_table.find_all('a',href=False):
        #         if a.has_attr("name") and a['name'].startswith("tt"):
        #             tt += str(each_table)

        # first_title = re.search(r'<td class="result_text">(.+?)</td>', tt).group(1)
        # print(first_title)
        # movie_name = str(re.search(r'>(.+?)<',first_title).group(1)).replace(" ","_")
        # print(movie_name)
        # title_id = ''
        # #extract title id from first title
        # for each in first_title.split("/"):
        #     if each.startswith("tt"):
        #         title_id += each
        # print(title_id)
        # #form user reviews link with title id
        # link = imdb["urv_link_part_1"]+title_id+imdb["urv_link_part_2"]
        # chrome_driver = webdriver.Chrome('/Users/eshwar/Documents/projects/sentiment_analysis_on_movie_reviews/reviews_scrape/reviews_scrape/spiders/chromedriver')
        # chrome_driver.get(link)
        # #scrape the link and redirect to scrape_reviews function
        #request = scrapy.Request(link, callback=self.scrape_reviews)
        #yield request

    def scrape_reviews(self, response):
        global movie_name
        global link
        #get total number of reviews
        num_of_reviews = response.xpath(imdb["number_of_reviews"]).extract()
        reviews_no = num_of_reviews[0].split()[0]
        print(reviews_no)
        load_no = int((int(reviews_no) - 25)/25)
        print(load_no)
