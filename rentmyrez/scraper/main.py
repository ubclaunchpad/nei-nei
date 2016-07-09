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
WebDriverWait(pjs, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'listing-address')))
# Scrolling
# Load all dynamic content using scrolling DOM actions
className = 'listings-container'
scrollName = 'may-scroll generic-list-container list-container'
execute = "var lastTopPos = document.getElementsByClassName('"+className+"')[1].lastElementChild.offsetTop; " + "document.getElementsByClassName('"+scrollName+"')[0].scrollTop = lastTopPos;"

# Loop to load as many postings as possible
finalNumPosts = 0
def checkIfMorePosts(browserObject, script, posts):
    # Render page as page_source and BS objects
    currSource = browserObject.page_source
    currBSObj  = BeautifulSoup(currSource)

    i = 0
    # Count all postings on current page
    for post in currBSObj.findAll("div", {"class":"listing-preview"}):
        i += 1
    print(str(i))
    # If the number of postings hasn't increased by the second iteration, return
    if i == posts or i > 2000:
        finalNumPosts = i
        return 1

    # Otherwise execute scrolling JavaScript again and recurse
    browserObject.execute_script(script)
    checkIfMorePosts(browserObject, script, i)


checkIfMorePosts(pjs, execute, 0)

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

def saveToDb(postings):
    import os, sys
    import django
    proj_path = '../../rentmyrez'
    sys.path.append(proj_path)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rentmyrez.settings')
    django.setup()
    from housing_heatmap.models import House
    for posting in postings:
        # check if posting url already exists in db.
        h = House(latitude=posting['latitude'],
                  longitude=posting['longitude'],
                  num_bedrooms=posting['numBeds'],
                  #square_footage=posting['squareFootage'],
                  #posted=posting['postingDate']
                  rent=posting['price'],
                  posting_url=posting['extURL'],
                  address=posting['listAddr'])
        h.save()
    # {"listAddr": "366 W 15th Ave, Vancouver, BC V5Y 1Y2", "numBeds": 1, "extURL": "https://www.padmapper.com/listings/16997061.-1-bedroom-1-bathroom-apartment-at-366-w-15th-ave-vancouver-bc-v5y-1y2", "longitude": "-123.113", "latitude": "49.2575", "price": 1700}

if __name__ == '__main__':
    rmr.getPostsFromPage(finalBSObj, postings)
    saveToDb(postings)

# Output file, temporary
with open('output.json', 'w') as fout:
    json.dump(postings, fout)

pjs.close()
