from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
import logging


# Get immediate child of listing-preview that contains URL to actual posting
#   Tag: a href="URL"
def getExtURL(post):
    extURL = post.find("a")['href']
    return extURL

# Get listing address
#   Tag: div class="listing-address"
#   Ex. Kitchener St, Vancouver, BC, V5K 3C8
def getListAddr(post):
    listAddr = post.find("div", {"class":"listing-address"}).get_text()
    return listAddr

# Get price per month
#   Tag: immediate div child of div class="listing-properties"
#   Ex. $706
def getPrice(post):
    price = post.find("div", {"class":"listing-properties"}).find("div").get_text()
    price = int(re.sub('[\$\,]', '', price))
    return price

# Get number of beds
#   Tag: div class="listing-num-bedrooms"
#   Ex. 1 Bed (Can be studio)
def getNumBeds(post):
    numBeds = post.find("div", {"class":"listing-num-bedrooms"}).get_text()
    studio = re.compile("[Sstudio]*?")
    if (studio.match(numBeds)): # studios are 1 br
        numBeds = 1
    else:
        numBeds = int(re.sub('[Beds]', '', numBeds.strip()))
    return numBeds

def getSquareFootage():
    pass

def getPostingDate():
    pass

# Now to step into each link for latitudes and longitudes
def getLatLonFromLink(webDriver, URL, *args):
    lat, lon = None, None
    try:
        time.sleep(11) # Scraper courtesy wait ~6 postings/minute
        webDriver.get(URL)
        html = webDriver.page_source
        bsObj = BeautifulSoup(html)
        # If the pair leads to an AirBnB page
        latLonTag = ""
        if (args[0].match(URL)):
            latLonTag = "airbedandbreakfast"
        # Otherwise the pair is a padmapper page
        else:
            latLonTag = "place"
        print(latLonTag)
        # Find latitude and longitude for a post
        # Each can be found in page metadata (super easy yay)
        lat = bsObj.find("meta", {"property":latLonTag+":location:latitude"})['content']
        lon = bsObj.find("meta", {"property":latLonTag+":location:longitude"})['content']

    except:
        logging.basicConfig(filename="get_latlon.log", level=logging.DEBUG)
        logging.exception('getLatLonFromLink()', exc_info=True)
    finally:
        return lat, lon

# Store general posting data in a list of dictionaries
def addPosting(webDriver, postingList, extURL, listAddr, price, numBeds):
    # Tag testing
    airbnb = re.compile(r"https\:\/\/(www\.)?airbnb\.com\/rooms\/[\w\?\&\-\=]*")
    lat, lon = getLatLonFromLink(webDriver, extURL, airbnb)

    if lat is None or lon is None:
        raise TypeError

    post = {
        "extURL":       str(extURL),
        "listAddr":     str(listAddr),
        #"postingDate":  str(postingDate), # TODO
        "price":        int(price),
        "numBeds":      int(numBeds),
        #"sqrFootage":   int(sqrFootage),  # TODO
        "latitude":     float(lat),
        "longitude":    float(lon)
    }
    postingList.append(post)
    # print ("Added a posting from URL: " + str(extURL))

# Get a posting preview div on page
#   Tag: div class="listing-preview"
def getPostsFromPage(webDriver, bsObject, postingList):
    successPosts   = 0
    latLonFailures = 0
    totalFailures  = 0
    for post in bsObject.findAll("div", {"class":"listing-preview"}):
        if (post.get_text() == ''): break # scraper has hit the last div so end
        try:
            addPosting(webDriver, postingList, getExtURL(post), getListAddr(post), getPrice(post), getNumBeds(post))
            successPosts += 1
        except TypeError:
            latLonFailures += 1
            logging.basicConfig(filename="get_posts.log", level=logging.DEBUG)
            logging.exception('getPostsFromPage(): addPosting(): lat or long is null', exc_info=True)
            pass
        except:
            totalFailures += 1
            logging.basicConfig(filename="get_posts.log", level=logging.DEBUG)
            logging.exception('getPostsFromPage(): addPosting(): complete failure to create post', exc_info=True)
            pass

    print("Finished storing " + str(successPosts) + " listings.")
    print("Failed to get latitude or longitude " + str(latLonFailures) + " times.")
    print("Failed to create posts " + str(totalFailures) + " times.")
