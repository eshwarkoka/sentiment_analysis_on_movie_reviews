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
    name = 'imdb_spider'
    allowed_domains = ["imdb.com"]
    start_urls = [
        'https://www.imdb.com/find?ref_=nv_sr_fn&q='
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url+self.ip+"&s=all" , dont_filter=True)

    def parse(self, response):
        global movie_name
        global link
        for url in self.start_urls:
            imdb_content = requests.get(url+self.ip+"&s=all")
        imdb_soup = BeautifulSoup(imdb_content.text, features='html.parser')
        #get all tables
        tables = imdb_soup.findAll("div",class_="findSection")
        #get tables which contains <a name="tt> </aa> because we want Titles, not Names
        tt = ""
        for each_table in tables:
            for a in each_table.find_all('a',href=False):
                if a.has_attr("name") and a['name'].startswith("tt"):
                    tt += str(each_table)

        first_title = re.search(r'<td class="result_text">(.+?)</td>', tt).group(1)
        print(first_title)
        movie_name = str(re.search(r'>(.+?)<',first_title).group(1)).replace(" ","_")
        print(movie_name)
        title_id = ''
        #extract title id from first title
        for each in first_title.split("/"):
            if each.startswith("tt"):
                title_id += each
        print(title_id)
        #form user reviews link with title id
        link = imdb["urv_link_part_1"]+title_id+imdb["urv_link_part_2"]
        chrome_driver = webdriver.Chrome('/Users/eshwar/Documents/projects/sentiment_analysis_on_movie_reviews/reviews_scrape/reviews_scrape/spiders/chromedriver')
        chrome_driver.get(link)
        #scrape the link and redirect to scrape_reviews function
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
        #chrome_driver = webdriver.Chrome('/Users/eshwar/Documents/projects/sentiment_analysis_on_movie_reviews/reviews_scrape/reviews_scrape/spiders/')
        # #get authors of reviews
        # authors = response.xpath(imdb["authors"]).extract()
        # #get review dates of reviews
        # review_dates = response.xpath(imdb["review_dates"]).extract()
        # #get titles of reviews
        # titles = response.xpath(imdb["titles"]).extract()
        # titles = [title.replace("\n","") for title in titles]
        # #get ratings of reviews
        # ratings = response.xpath(imdb["ratings"]).extract()
        # del ratings[1::2]
        # #get reviews
        # reviews = response.xpath(imdb["reviews"]).extract()
        # start_review = r'<div class="text show-more__control">'
        # end_review = r'</div>'
        # reviews_list = []
        #
        # for each_review in reviews:
        #     temp_review = each_review[each_review.find(start_review) + len(start_review):each_review.find(end_review)]
        #     temp_review = temp_review.replace("<br>", "")
        #     temp_review = temp_review.replace("</br>", "")
        #     reviews_list.append(temp_review)
        #
        # reviews = reviews_list
        # del reviews_list
        #
        # json_data = [
        #     {
        #         "author" : a,
        #         "review_date" : rd,
        #         "title" : t,
        #         "rating" : ra,
        #         "review" : re
        #     } for a, rd, t, ra, re in zip(authors, review_dates, titles, ratings, reviews)
        # ]
        #
        # project_path = r'/Users/eshwar/Documents/projects/sentiment_analysis_on_movie_reviews/'
        # target_path = project_path+"data/scraped_reviews/"
        # output_filename = target_path+movie_name+".json"
        # with open(output_filename, 'w') as f:
        #     json.dump(json_data, f, ensure_ascii=False, indent=4)
        # with open(target_path+"temp.txt", 'w') as f:
        #     f.write(movie_name)