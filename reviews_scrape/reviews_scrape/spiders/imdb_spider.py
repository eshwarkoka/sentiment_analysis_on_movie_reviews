import scrapy
import unicodedata

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
        filename = 'first_title_id.txt'
        first_title = response.xpath('(//td[@class="result_text"])[1]').extract()
        first_title = str(first_title[0])
        splitted = first_title.split("/")
        title_id = ''
        for each in splitted:
            if each.startswith("tt"):
                title_id += each
        with open(filename, 'w') as f:
            f.write(title_id)
        link = "https://www.imdb.com/title/"+title_id+"/reviews?ref_=tt_urv"
        request = scrapy.Request(link, callback=self.scrape_reviews)
        yield request

    def scrape_reviews(self, response):
        titles = response.xpath('//a[@class="title"]/text()').extract()
        ratings = response.xpath('//span[@class="rating-other-user-rating"]//span//text()').extract()
        del ratings[1::2]
        reviews = response.xpath('//div[@class="content"]').extract()
        start_review = r'<div class="text show-more__control">'
        end_review = r'</div>'
        reviews_list = []

        for each_review in reviews:
            temp_review = each_review[each_review.find(start_review) + len(start_review):each_review.find(end_review)]
            temp_review = temp_review.replace("<br>", "")
            temp_review = temp_review.replace("</br>", "")
            reviews_list.append(temp_review)

        for i in range(0,25):
            yield {
                "title" : titles[i],
                "rating" : ratings[i],
                "review" : reviews_list[i]
            }
        # with open(filename, 'w') as f:
        #     for each in titles:
        #         f.write(each)
        #     for each in ratings:
        #         f.write(each+"\n")
        #     for each_review in reviews_list:
        #         f.write(each_review+"\n*******************\n")
        #         #f.write(each[each.find(string_start)+len(string_start):each.find(string_end)]+"\n**********************\n")
        #         #f.write(each+"\n*******************\n")