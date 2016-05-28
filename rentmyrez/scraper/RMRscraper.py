from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
import pymysql
import time
import re

# PyMySQL connects scraper to MySQL database
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='XXXX', # use your local db's pw
                       db='mysql')      # keep this

curr = conn.cursor()
curr.execute("USE RMRscraper")

# Generate SQL queries
# Note: add imgPath once a filing system for images of rentals has been defined
def store(extURL, listAddr, price, numBeds):
    curr.execute("INSERT INTO listings (extURL, listAddr, price, numBeds) VALUES (\"%s\", \"%s\", \"%s\", \"%s\")", (extURL, listAddr, price, numBeds))
    curr.connection.commit()
    # curr.execute("ALTER IGNORE TABLE listings ADD UNIQUE (extURL)", (extURL))
    # curr.connection.commit()

# Selenium and PhantomJS needed to execute JavaScript and render AJAX-enabled dynamic pages
pjs = webdriver.PhantomJS()
# pjs.get("https://www.padmapper.com/?viewType=LIST&lat=49.222899&lng=-123.038579&zoom=10&minRent=100&maxRent=5000&minBR=0&maxBR=10&minBA=1&cats=false&dogs=false")
pjs.get("file:///home/estro/GitHub/rent-my-rez/rentmyrez/scraper/sample.html")
pageSource = pjs.page_source

# Create a BS object from driver's page source
bsObj = BeautifulSoup(pageSource)

# Get immediate child of listing-preview that contains URL to actual posting
#   Tag: a href="URL"
def getExtURL(post):
    extURL = post.find("a")
    extURL = extURL['href']
    return extURL

# Get listing pic
#   Tag: div class="listing-image" data-original="PIC URL"
# def getListImg(post):
#     listImg = post.find("div", {"class":"listing-image"})
#     listImg = listImg['data-original']
#     #print("URL found:", listImg)
#     return listImg

# Get listing address
#   Tag: div class="listing-address"
#   Ex. Kitchener St, Vancouver, BC, V5K 3C8
def getListAddr(post):
    listAddr = post.find("div", {"class":"listing-address"}).get_text()
    #print("Listing Address found:", listAddr)
    return listAddr

# Get price per month
#   Tag: immediate div child of div class="listing-properties"
#   Ex. $706
def getPrice(post):
    price = post.find("div", {"class":"listing-properties"}).find("div").get_text()
    price = int(re.sub('[\$\,]', '', price))
    #print("Listing Address found:", price)
    return price

# Get number of beds
#   Tag: div class="listing-num-bedrooms"
#   Ex. 1 Bed (Can be studio)
def getNumBeds(post):
    numBeds = post.find("div", {"class":"listing-num-bedrooms"}).get_text()
    studio = re.compile("[Studio]*?")
    if (studio.match(numBeds)): # studios are 1 br
        numBeds = 1
    else:
        numBeds = int(re.sub('[Beds]', '', numBeds.strip()))
    #print("Listing Address found:", numBeds)
    return numBeds

posts = 0
# Get a posting preview div on page
#   Tag: div class="listing-preview"
for post in bsObj.findAll("div", {"class":"listing-preview"}):
    if (post.get_text() == ''): break # scraper has hit the last div so end
    try:
        store(getExtURL(post), getListAddr(post), getPrice(post), getNumBeds(post))
        posts += 1
    except TypeError:
        pass

print("Finished storing " + str(posts) + " listings")

pjs.close()
curr.close()
conn.close()
