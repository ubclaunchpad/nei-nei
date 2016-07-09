import RMRScraper_utils as rmr
import calc_coords as cc
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

# display = Display(visible=0, size=(1024,768))
# display.start()

# Selenium and PhantomJS needed to execute JavaScript and render AJAX-enabled dynamic pages
driver = webdriver.PhantomJS()

def calculateSectorURLs(lat, lon, zoom):
    startLat = str(lat)
    startLon = str(lon)
    newZoom  = str(zoom)
    sectors = []
    for sector in cc.mapSectors(sectors, startLat, startLon, 12):
        nextSector = "https://www.padmapper.com/?viewType=LIST&lat="
        + sector['latitude'] + "&lng=" + sector['longitude'] + "&zoom="
        + newZoom + "&minRent=100&maxRent=5000&minBR=0&maxBR=10&minBA=1&cats=false&dogs=false"
        sectors.append(sector)
    return sectors

def scrapeSector(sector):
    driver.get(sector)
    # Wait until div's of the class 'listing-address' are present before grabbing source
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'listing-address')))
    # Scrolling
    # Load all dynamic content using scrolling DOM actions
    element = driver.find_element_by_class_name("list-container")
    scroll_height = driver.execute_script('return document.getElementsByClassName("list-container")[0].scrollHeight')
    scroll_height_prev = 0
    # Loop to load as many postings as possible
    while scroll_height != scroll_height_prev:
        finalNumPosts = 0
        pageSource = driver.page_source
        bsObj = BeautifulSoup(pageSource, "html.parser")
        for post in bsObj.findAll("div", {"class": "listing-preview"}):
            finalNumPosts += 1
        driver.execute_script('document.getElementsByClassName("list-container")[0].scrollTop = document.getElementsByClassName("list-container")[0].scrollHeight')
        scroll_height_prev = scroll_height
        time.sleep(3) # Scraper courtesy wait
        scroll_height = driver.execute_script('return document.getElementsByClassName("list-container")[0].scrollHeight')
        print("Scroll height is " + str(scroll_height))

    # Final page_source and BS objects after all scrolling complete
    finalSource = driver.page_source
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

    rmr.getPostsFromPage(finalBSObj, postings)

    # Output file, temporary
    with open('output.json', 'a') as fout:
        json.dump(postings, fout)

if __name__ == '__main__':
    lat = 49.251756
    lon = -123.053441
    zoom = 12
    sectors = calculateSectorURLs(lat, lon, zoom)
    for sector in sectors:
        scrapeSector(sector)

driver.quit()
# display.close()
