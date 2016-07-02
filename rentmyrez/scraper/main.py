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
pjs.get("https://www.padmapper.com/?viewType=LIST&lat=49.255230&lng=-123.075677&zoom=12&minRent=100&maxRent=10000&minBR=0&maxBR=10&minBA=1&cats=false&dogs=false")
# Wait until div's of the class 'listing-address' are present before grabbing source
WebDriverWait(pjs, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'listing-address')))
# Scrolling
# Load all dynamic content using scrolling DOM actions
className = 'listings-container'
scrollName = 'may-scroll generic-list-container list-container'
execute = "var lastTopPos = document.getElementsByClassName('"+className+"')[1].lastElementChild.offsetTop; " + "document.getElementsByClassName('"+scrollName+"')[0].scrollTop = lastTopPos;"

finalNumPosts = 0
def checkIfMorePosts(browserObject, script, posts):

    currSource = browserObject.page_source
    currBSObj  = BeautifulSoup(currSource)

    i = 0
    for post in currBSObj.findAll("div", {"class":"listing-preview"}):
        i += 1
    print(str(i))
    if i == posts or i > 2000:
        finalNumPosts = i
        return 1

    browserObject.execute_script(script)
    checkIfMorePosts(browserObject, script, i)


checkIfMorePosts(pjs, execute, 0)

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

with open('output.json', 'w') as fout:
    json.dump(postings, fout)

pjs.close()
