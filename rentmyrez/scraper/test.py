from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# Selenium and PhantomJS needed to execute JavaScript and render AJAX-enabled dynamic pages
pjs = webdriver.PhantomJS()
#pjs.implicitly_wait(10) # selenium implicit wait for listings to load
pjs.get("https://www.padmapper.com/?viewType=LIST&lat=49.222899&lng=-123.038579&zoom=10&minRent=100&maxRent=5000&minBR=0&maxBR=10&minBA=1&cats=false&dogs=false")
time.sleep(5)
# try:
#     testElement = WebDriverWait(pjs, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'listing-preview')))
#     print("Wait executed")
# except TimeOutException:
#     print("Timeout experienced")
# finally:
pageSource = pjs.page_source
bsObj = BeautifulSoup(pageSource)
for post in bsObj.findAll('div', {'class','listing-preview'}):
    print(post)
pjs.close()
