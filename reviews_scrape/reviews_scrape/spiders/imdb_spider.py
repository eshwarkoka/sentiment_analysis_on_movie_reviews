import scrapy
import json

with open('./locators/xpaths.json') as f:
    xpaths = json.load(f)

imdb = xpaths["imdb"][0]

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
        #get first title from all titles
        first_title = str(response.xpath(imdb["first_title"]).extract())
        title_id = ''
        #extract title id from first title
        for each in first_title.split("/"):
            if each.startswith("tt"):
                title_id += each
        #form user reviews link with title id
        link = imdb["urv_link_part_1"]+title_id+imdb["urv_link_part_2"]
        #scrape the link and redirect to scrape_reviews function
        request = scrapy.Request(link, callback=self.scrape_reviews)
        yield request

    def scrape_reviews(self, response):
        #get authors of reviews
        authors = response.xpath(imdb["authors"]).extract()
        #get review dates of reviews
        review_dates = response.xpath(imdb["review_dates"]).extract()
        #get titles of reviews
        titles = response.xpath(imdb["titles"]).extract()
        titles = [title.replace("\n","") for title in titles]
        #get ratings of reviews
        ratings = response.xpath(imdb["ratings"]).extract()
        del ratings[1::2]
        #get reviews
        reviews = response.xpath(imdb["reviews"]).extract()
        start_review = r'<div class="text show-more__control">'
        end_review = r'</div>'
        reviews_list = []

        for each_review in reviews:
            temp_review = each_review[each_review.find(start_review) + len(start_review):each_review.find(end_review)]
            temp_review = temp_review.replace("<br>", "")
            temp_review = temp_review.replace("</br>", "")
            reviews_list.append(temp_review)

        reviews = reviews_list
        del reviews_list

        json_data = [
            {
                "author" : a,
                "review_date" : rd,
                "title" : t,
                "rating" : ra,
                "review" : re
            } for a, rd, t, ra, re in zip(authors, review_dates, titles, ratings, reviews)
        ]

        target_path = r'./target/'
        output_filename = target_path+self.ip+".json"
        with open(output_filename, 'w') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)