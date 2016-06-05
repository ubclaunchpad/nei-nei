from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
import pymysql
import time
import re
import logging

# PyMySQL connects scraper to MySQL database
connection = pymysql.connect(host='localhost',
                       user='root',
                       password='&L4u*cHp4d', # use your local db's pw
                       db='mysql')      # keep this

cursor = connection.cursor()
cursor.execute("USE RMRscraper")

# Generate SQL queries
# Note: add imgPath once a filing system for images of rentals has been defined
def storePrelim(extURL, listAddr, price, numBeds):
    standard = re.compile("http\:\/\/[(www)?\.[(padmapper\.com\/listings\/[\d\w\.\-\=]*) || (airbnb\.com\/rooms\/[\d\w\?\-\=]*)")
    if not (standard.match(extURL)): extURL = NULL
    cursor.execute("INSERT INTO listings (extURL, listAddr, price, numBeds) VALUES (\"%s\", \"%s\", %s, %s)", (extURL, listAddr, price, numBeds))
    cursor.connection.commit()

    #TODO: only add new postings if link is not present in the table
    # cursor.execute("ALTER IGNORE TABLE listings ADD UNIQUE extURL", extURL)
    # cursor.connection.commit()

def storeLatLon(lat, lon, lid):
    cursor.execute("UPDATE listings SET latitude=%(lat)s, longitude=%(lon)s WHERE listingID = %(lid)s", {'lat':lat, 'lon':lon, 'lid':lid})
    cursor.connection.commit()

def getURLs():
    cursor.execute("SELECT listingID, extURL FROM listings WHERE extURL IS NOT NULL")
    links = cursor.fetchall()
    return links

# Selenium and PhantomJS needed to execute JavaScript and render AJAX-enabled dynamic pages
pjs = webdriver.PhantomJS()
pjs.get("https://www.webpage.com")
pageSource = pjs.page_source

# Scrolling function
# TODO: use PhantomJS' scrollTop property to load all dynamic content


# Create a BS object from driver's page source
bsObj = BeautifulSoup(pageSource)

# Get immediate child of listing-preview that contains URL to actual posting
#   Tag: a href="URL"
def getExtURL(post):
    extURL = post.find("a")
    extURL = extURL['href']
    return extURL

# TODO: Get listing pic
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

# Get a posting preview div on page
#   Tag: div class="listing-preview"
posts = 0
for post in bsObj.findAll("div", {"class":"listing-preview"}):
    if (post.get_text() == ''): break # scraper has hit the last div so end
    try:
        storePrelim(getExtURL(post), getListAddr(post), getPrice(post), getNumBeds(post))
        posts += 1
    except:
        logging.basicConfig(filename="store_prelim.log", level=logging.DEBUG)
        logging.exception('storePrelim()', exc_info=True)
        pass

print("Finished storing " + str(posts) + " listings.")

# Now to step into each link for latitudes and longitudes
# DB will be updated on each link entry
numLinks = 0
listToCrawl = getURLs()
print("Finding latitudes and longitudes for " + str(len(listToCrawl)) + " listings.")
for pair in listToCrawl: # pair[1] gets the url from returned tuples
    airbnb = re.compile("http\:\/\/[(www)?\.airbnb\.com\/rooms\/[\d\w\?\-\=]*")
    # Load pair into PhantomJS
    lid  = pair[0]
    link = str(pair[1])
    print(link)
    try:
        html = urlopen(link)
        bsObj = BeautifulSoup(html)
        # If the pair leads to an AirBnB page
        if (airbnb.match(link)):
            latLonTag = "airbedandbreakfast"
        # Otherwise the pair is a padmapper page
        else:
            latLonTag = "place"
        # Find latitude and longitude for a post
        # Each can be found in page metadata (super easy yay)
        lat = bsObj.find("meta", {"property":latLonTag+":location:latitude"})['content']
        lon = bsObj.find("meta", {"property":latLonTag+":location:longitude"})['content']
        try:
            storeLatLon(lat, lon, lid)
            numLinks += 1
        except: # if an exception is raised, record traceback
            logging.basicConfig(filename="store_latlon.log", level=logging.DEBUG)
            logging.exception('storeLatLon()', exc_info=True)
            pass
    except URLError:
        pass

print("Finished finding latitudes and longitudes for " + str(numLinks) + " listings.")
pjs.close()
cursor.close()
connection.close()
