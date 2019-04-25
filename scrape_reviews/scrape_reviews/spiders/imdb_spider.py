import scrapy,json,re,time,os,glob
from scrapy.exceptions import CloseSpider
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

#get all the imdb xpaths from xpaths.json file
with open('./locators/xpaths.json') as f:
    xpaths = json.load(f)
imdb = xpaths["imdb"][0]

#define all the required variables
movie_name = ''
project_path = r'/Users/eshwar/Documents/projects/sentiment_analysis_on_movie_reviews/'
scraped_reviews_path = project_path + "data/scraped_reviews/"
predicted_reviews_path = project_path + "data/predicted_reviews/"
chrome_driver_path = project_path+"scrape_reviews/chrome_driver/chromedriver"

class IMDBSpider(scrapy.Spider):
    name = 'imdb_spider'
    allowed_domains = ["imdb.com"]
    start_urls = [
        'https://www.imdb.com/find?ref_=nv_sr_fn&q='
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url+self.ip+"&s=tt" , dont_filter=True)

    def parse(self, response):
        #get all the globally defined variables
        global movie_name, project_path, scraped_reviews_path, chrome_driver_path

        #get first title
        first_title = response.xpath(imdb["first_title"]).extract()

        #extract title id from first title
        for each_split in first_title[0].split("/"):
            if each_split.startswith("tt"):
                title_id = each_split

        #extract movie name from first title
        movie_name = str(re.search(r'">(.+?)</a>', str(first_title[0])).group(1)).replace(" ","_")
        temp_movie_name = movie_name

        #put timestamp
        epoch = time.time()
        movie_name+="$#$"+str(epoch)

        # create temp file to store movie name temporarily
        with open(scraped_reviews_path + "temp.txt", 'w') as f:
            f.write(movie_name)

        #check timestamp
        current_dir = os.getcwd()
        change_dir = scraped_reviews_path
        os.chdir(change_dir)
        temp = temp_movie_name+"$#$"
        old_file_name = glob.glob(temp+"*")
        diff = 0
        #flag determines if searched movie is already searched within a week or not
        #flag = 0 (file available)
        #flag = 1 (new search)
        flag = 1
        if len(old_file_name) > 0:
            old_file_name = old_file_name[0]
            old_timestamp = old_file_name.split("$#$")[1][:-5]
            diff = epoch - float(old_timestamp)
            if diff < 604800:
                flag = 0
                with open(project_path+"flag.txt", "w") as f:
                    f.write(str(flag))
                raise CloseSpider('file available')
            else:
                os.remove(scraped_reviews_path+old_file_name)
                os.remove(predicted_reviews_path+old_file_name)
        os.chdir(current_dir)

        #form imdb reviews link
        reviews_link = imdb["urv_link_part_1"] + title_id + imdb["urv_link_part_2"]

        #get chrome driver executable
        options = Options()
        options.headless = True
        chrome_driver = webdriver.Chrome(chrome_driver_path, chrome_options=options)

        #go to reviews link
        chrome_driver.get(reviews_link)

        #click load more button until the button exists
        while True:
            try:
                WebDriverWait(chrome_driver, 10).until(EC.element_to_be_clickable((By.XPATH, imdb["load_more_button"]))).click()
            except TimeoutException as ex:
                break

        #get the number of reviews
        num_of_reviews = chrome_driver.find_element_by_xpath(imdb["number_of_reviews"]).text
        reviews_no = num_of_reviews.split()[0]
        print(reviews_no)

        #open all the spoilers
        spoiler_click = chrome_driver.find_elements_by_xpath(imdb["spoiler_open"])
        for i in range(0, len(spoiler_click)):
            if spoiler_click[i].is_displayed():
                spoiler_click[i].click()

        #get all the reviews
        reviews = chrome_driver.find_elements_by_xpath(imdb["reviews"])

        #convert reviews to list
        reviews_list = [str(review.text).replace("\n"," ") for review in reviews]

        #get all the authors
        authors = chrome_driver.find_elements_by_xpath(imdb["authors"])

        #convert authors to list
        authors_list = [a.text for a in authors]

        #get all the review dates
        review_dates = chrome_driver.find_elements_by_xpath(imdb["review_dates"])

        #convert review dates to list
        review_dates_list = [rd.text for rd in review_dates]

        #get all the titles
        titles = chrome_driver.find_elements_by_xpath(imdb["titles"])

        #convert titles to list
        titles_list = [str(t.text).replace("\n", " ") for t in titles]

        #create json_data variable with authors, review dates, titles and reviews
        json_data = [
            {
                "author" : a,
                "review_date" : rd,
                "title" : t,
                "review" : re
            } for a, rd, t, re in zip(authors_list, review_dates_list, titles_list, reviews_list)
        ]

        output_filename = scraped_reviews_path + movie_name + ".json"
        with open(output_filename, 'w') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        #close the chrome driver
        chrome_driver.close()
