from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from craigslist.items import CraigslistItem


class MySpider(CrawlSpider):
    name = "craigs"
    allowed_domains = ["sfbay.craigslist.org"]
    start_urls = ["https://sfbay.craigslist.org/search/apa"]

    rules = (
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//a[@class="button next"]',)), callback="parse_items",
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
            if len(item["datetime"]) == 0 or len(item["price"]) == 0:
                continue
            item["location"] = info.xpath('span[@class="pnr"]/small/text()').extract()
            item["room"] = info.xpath('span[@class="housing"]/text()').extract()
            item["area"] = info.xpath('span[@class="housing"]/text()').extract()
            items.append(item)
        return items


    def parse_items_css(self, response):
        times = response.css('span.pl')
        infos = response.css('span.l2')
        items = []
        for time, info in zip(times, infos):
            item = CraigslistItem()
            item["datetime"] = time.css('time::attr("datetime")').extract()
            item["price"] = info.css('span.price::text').extract()
            if len(item["datetime"]) == 0 or len(item["price"]) == 0:
                continue
            item["location"] = info.css('span.pnr small::text').extract()
            item["room"] = info.css('span.housing::text').extract()
            item["area"] = info.css('span.housing::text').extract()
            items.append(item)
        return items