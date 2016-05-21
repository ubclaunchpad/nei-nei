from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re

# Create initial url to scrape and a BS object from that url
html = urlopen("https://...")
bsObj = BeautifulSoup(html)

# Steps into each link on a page
#   When each link has be searched, move on to next page
#   Stop searching when post time > 7 days old


# Searches each page link for UBC residences (unnecessary if looking in a broader scope)
#   If residence is listed on UBC campus as one of:
#       Marine Drive, Thunderbird, Ponderosa Commons, Fraser Hall
#   find:
#       pricing information, number of rooms in residence (can be null), type of room (studio/single), GPS (can be null), furnished flag, picture (can be null), availability
#   else go to next link on page


# Find posting date
#   Tag order: body -> section id="pagecontainer" -> section class="body" -> section class="userbody" -> div class="postinginfos" -> p class="postinginfo" -> time
#   Form: YEAR-MONTH-DAY H:MM(pm|am)


# Find pricing information
#   Tag order: body -> section id="pagecontainer" -> section class="body" -> h2 class="postingtitle" -> span class="postingtitletext" -> span class="price"
#   Form: \$\d+ ex. $1350


# Find number of rooms, baths in residence
#   Tag order: body -> section id="pagecontainer" -> section class="body" -> h2 class="postingtitle" -> span class="postingtitletext" -> span class="housing"
#   Form: \/\s(\d){0,2}(br)?\s-\s(\d+ft)*
#   Alt tag order: body -> section id="pagecontainer" -> section class="body" -> section class="userbody" -> div class="mapAndAttrs" -> p class="attrgroup" (2nd one) -> span -> b BR b Ba-> br -> span -> b \d+



# Find type of room
#   Tag order: body -> section id="pagecontainer" -> section class="body" -> h2 class="postingtitle" -> span class="postingtitletext" -> span class="housing" -> span id="titletextonly"


# Find GPS/Google maps
#   Tag order: body -> section id="pagecontainer" -> section class="body" -> section class="userbody" -> div class="mapAndAttrs" -> div class="mapbox" -> (div id="map" data-latitude="\d{1,3}\.\d+" data-longitude="\d{1,3}\.\d+") || (p class="mapaddress" -> small -> a href="https://maps.google.com/[\w\d\%\+\-\=]+")


# Find furnishing information (smoking, pets etc.)
#   Tag order: body -> section id="pagecontainer" -> section class="body" -> section class="userbody" -> div class="mapAndAttrs" -> p class="attrgroup" (2nd one) -> span -> br -> span ...


# Find picture(s)
#   Tag order: body -> section id="pagecontainer" -> section class="body" -> section class="userbody" -> figure class="iw multiimage" -> div class="gallery" -> div class="swipe" -> div class="swipe-wrap" -> div class="slide first visible" -> img src="URL we want"


# Find availability
#   Tag order: body -> section id="pagecontainer" -> section class="body" -> section class="userbody" -> div class="mapAndAttrs" -> p class="attrgroup" (1st one) -> span class="housing_movein_now property_date" date="20\d{2}-\d\d-\d\d"
