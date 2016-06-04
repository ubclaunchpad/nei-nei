from scrapy.contrib.spiders import CrawlSpider, Rule
from RMRSpider.items import RmrspiderItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class RMRSpider(CrawlSpider):
    name = "post"
    allowed_domains = ["vancouver.craigslist.ca"]
    start_urls = ["https://vancouver.craigslist.ca/search/apa"]
    rules = [Rule(SgmlLinkExtractor(allow=('(/\w{1,4}/)?/apa(\?s=\d*)?/\d*.html'),), callback="parse_item", follow=True)]

    def parse_item(self, response):
        item = RmrspiderItem()
        title = response.xpath('//h1/text()')[0].extract()
        item['title'] = title
        return item
