from urllib2 import urlopen
from urllib2 import HTTPError, URLError
import urlparse
from bs4 import BeautifulSoup
import time
import re
import logging

# Get immediate child of listing-preview that contains URL to actual posting
#   Tag: a href="URL"
def getExtURL(post):
    extURL = post.find("a")['href']
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
    studio = re.compile("[Studio]*?")
    if (studio.match(numBeds)): # studios are 1 br
        numBeds = 1
    else:
        numBeds = int(re.sub('[Beds]', '', numBeds.strip()))
    return numBeds

# Now to step into each link for latitudes and longitudes
def getLatLonFromLink(URL, args):
    lat, lon = None, None
    try:
        html = urlopen(URL)
        bsObj = BeautifulSoup(html)
        # If the pair leads to an AirBnB page
        if (args.match(URL)):
            latLonTag = "airbedandbreakfast"
        # Otherwise the pair is a padmapper page
        else:
            latLonTag = "place"
        # Find latitude and longitude for a post
        # Each can be found in page metadata (super easy yay)
        lat = bsObj.find("meta", {"property":latLonTag+":location:latitude"})['content']
        lon = bsObj.find("meta", {"property":latLonTag+":location:longitude"})['content']
    except URLError:
        logging.basicConfig(filename="get_latlon.log", level=logging.DEBUG)
        logging.exception('getLatLonFromLink()', exc_info=True)
    finally:
        return lat, lon

# Store general posting data
# Note: add imgPath once a schema addition for images of rentals has been defined
def addPosting(postingList, extURL, listAddr, price, numBeds):
    airbnb = re.compile(r"http\:\/\/(www\.)?airbnb\.com\/rooms\/[\w\?\&\-\=]*")
    lat, lon = getLatLonFromLink(extURL, airbnb)

    post = {
        "extURL":       extURL,
        "listAddr":     listAddr,
        "price":        price,
        "numBeds":      numBeds,
        "latitude":     lat,
        "longitude":    lon
    }
    postingList.append(post)
    print ("Added a posting from URL: " + str(extURL))

# Get a posting preview div on page
#   Tag: div class="listing-preview"
def getPostsFromPage(bsObject, postingList):
    posts = 0
    fails = 0
    for post in bsObject.findAll("div", {"class":"listing-preview"}):
        if (post.get_text() == ''): break # scraper has hit the last div so end
        try:
            addPosting(postingList, getExtURL(post), getListAddr(post), getPrice(post), getNumBeds(post))
            posts += 1
        except:
            fails += 1
            logging.basicConfig(filename="get_posts.log", level=logging.DEBUG)
            logging.exception('getPostsFromPage(): addPosting()', exc_info=True)
            pass

    print("Finished storing " + str(posts) + " listings.")
    print("Failed " + str(fails) + " times.")
