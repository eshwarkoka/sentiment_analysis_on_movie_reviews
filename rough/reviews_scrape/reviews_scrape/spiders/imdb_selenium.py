from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


imdb_url = "https://www.imdb.com/"

chrome_driver = webdriver.Chrome('/Users/eshwar/Documents/projects/sentiment_analysis_on_movie_reviews/reviews_scrape/reviews_scrape/spiders/chromedriver')
chrome_driver.get(imdb_url)
search = chrome_driver.find_element_by_name('q')
search.send_keys("robo")
chrome_driver.find_element_by_xpath("//select[@name='s']/option[text()='Titles']").click()
chrome_driver.find_element_by_xpath("//div[@class='magnifyingglass navbarSprite']").click()
chrome_driver.find_element_by_xpath("(//td[@class='result_text'])[1]/a").click()
chrome_driver.find_element_by_xpath("//a[contains(@href,'/reviews?ref_=tt_urv')]").click()
#load_more = chrome_driver.find_element_by_xpath("//button[@class='ipl-load-more__button']")
while True:
    WebDriverWait(chrome_driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='ipl-load-more__button']"))).click()
    #load_more = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ipl-load-more__button")))
    #load_more = chrome_driver.execute_script("document.getElementsbyClassName('ipl-load-more__button')[0].click()")
    #//button[@class='ipl-load-more__button']
    #load_more.click()



#chrome_driver.close()