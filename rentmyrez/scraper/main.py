import RMRScraper_utils as rmr
from functools import partial
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# Selenium and PhantomJS needed to execute JavaScript and render AJAX-enabled dynamic pages
pjs = webdriver.PhantomJS()
pjs.get("https://www.padmapper.com/?viewType=LIST&lat=49.273800&lng=-123.161000&zoom=12&minRent=100&maxRent=5000&minBR=0&maxBR=10&minBA=1&cats=false&dogs=false")
# Wait until div's of the class 'listing-address' are present before grabbing source
WebDriverWait(pjs, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'listing-address')))
# Scrolling
# Load all dynamic content using scrolling DOM actions
element = pjs.find_element_by_class_name("list-container")
scroll_height = pjs.execute_script('return document.getElementsByClassName("list-container")[0].scrollHeight')
scroll_height_prev = 0
# Loop to load as many postings as possible
while(scroll_height != scroll_height_prev):
    finalNumPosts = 0
    pageSource = pjs.page_source
    bsObj = BeautifulSoup(pageSource, "html.parser")
    for post in bsObj.findAll("div", {"class": "listing-preview"}):
        finalNumPosts += 1
    pjs.execute_script('document.getElementsByClassName("list-container")[0].scrollTop = document.getElementsByClassName("list-container")[0].scrollHeight')
    scroll_height_prev = scroll_height
    scroll_height = pjs.execute_script('return document.getElementsByClassName("list-container")[0].scrollHeight')
    print("Scroll height is " + str(scroll_height))

# Final page_source and BS objects after all scrolling complete
finalSource = pjs.page_source
finalBSObj  = BeautifulSoup(finalSource)

print("Final number of posts found: "+ str(finalNumPosts))

# List of dictionaries, each describing a post, with the form:
# [{
#     "extURL":       extURL,
#     "listAddr":     listAddr,
#     "price":        price,
#     "numBeds":      numBeds,
#     "latitude":     latitude,
#     "longitude":    longitude
# }]
postings = []

if __name__ == '__main__':
    rmr.getPostsFromPage(finalBSObj, postings)

# Output file, temporary
with open('output.json', 'w') as fout:
    json.dump(postings, fout)

pjs.close()
