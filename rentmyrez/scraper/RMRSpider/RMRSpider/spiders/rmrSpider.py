from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from RMRSpider.items import RmrSpiderItem
from selenium import webdriver

# Selenium and PhantomJS needed to execute JavaScript and render AJAX-enabled dynamic pages
pjs = webdriver.PhantomJS()
pjs.get("https://www.webpage.com")
pageSource = pjs.page_source

class RMRSpider(CrawlSpider):
    name = "rmrspider"
    allowed_domains = ["https://www.padmapper.com", "https://www.airbnb.com/rooms"]
    start_urls = ["https://www.padmapper.com/?viewType=LIST&lat=49.222899&lng=-123.038579&zoom=10&minRent=100&maxRent=5000&minBR=0&maxBR=10&minBA=1&cats=false&dogs=false"]
    rules = (
        # AirBnB
        Rule(SgmlLinkExtractor(allow=('(/rooms/[\d\w\?\-\=]*)'), ), callback="parse_bnb", follow=True),

        # Padmapper (posts on site)
        Rule(SgmlLinkExtractor(allow=('(/listings/[\d\w\.\-\=]*)'), ), callback="parse_pm", follow=True)
    )

    # AirBnB-specific parser
    def parse_bnb(self, response):
        # Define spider item, created by extracting data from HTML tags
        item = RmrSpiderItem()

        # Data selectors
        item['latitude']  = response.xpath('//meta[@property="airbedandbreakfast:location:latitude"]/@content/text()').extract()
        item['longitude'] = response.xpath('//meta[@property="airbedandbreakfast:location:longitude"]/@content/text()').extract()
        return item

    # Padmapper-specific parser
    def parse_pm(self, response):
        # Define spider item, created by extracting data from HTML tags
        item = RmrSpiderItem()

        # Data selectors
        item['latitude']  = response.xpath('//meta[@property="place:location:latitude"]/@content/text()').extract()
        item['longitude'] = response.xpath('//meta[@property="place:location:longitude"]/@content/text()').extract()
        return item
