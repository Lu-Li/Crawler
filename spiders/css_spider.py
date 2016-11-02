from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from craigslist.items import CraigslistItem


class CssSpider(CrawlSpider):
    name = "craigscss"
    allowed_domains = ["sfbay.craigslist.org"]
    start_urls = ["https://sfbay.craigslist.org/search/sby/apa?sale_date=2016-11-02&sort=upcoming"]

    rules = (
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//a[@class="next day "]',)), callback="parse_items",
             follow=True),
    )

    def parse_items(self, response):
        hxs = HtmlXPathSelector(response)
        times = hxs.xpath('//span[@class="pl"]')
        infos = hxs.xpath('//span[@class="l2"]')
        items = []
        for time, info in zip(times, infos):
            item = CraigslistItem()
            item["datetime"] = time.xpath('time/@datetime').extract()
            item["price"] = info.xpath('span[@class="price"]/text()').extract()
            item["location"] = info.xpath('span[@class="pnr"]/small/text()').extract()
            item["room"] = info.xpath('span[@class="housing"]/text()').extract()
            if len(item["datetime"]) == 0 or len(item["price"]) == 0 or len(item["room"]) == 0:
                continue
            item["area"] = info.xpath('span[@class="housing"]/text()').extract()
            items.append(item)
        return items
