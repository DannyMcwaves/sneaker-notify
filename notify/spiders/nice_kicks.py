from scrapy import Spider, signals
from ..items import NiceKicksItem
from datetime import datetime
from notify.slack import Slack
from config import APIKEY
from scrapy_splash import SplashRequest
from w3lib.http import basic_auth_header
from pprint import pprint
import logging


niceKicksUrl = "https://shopnicekicks.com/collections/new-arrivals-1"
niceKicksSlackContainer = Slack()
niceKicksSlackContainer.add_data("text", "*Now and upcoming stock on Rise45* :tada::tada:")


class NiceKicksSpider(Spider):
	name = "niceKicks"
	allowed_domains = ["shopnicekicks.com"]
	start_urls = [niceKicksUrl]

	def __init__(self):
		super(NiceKicksSpider, self).__init__()
		self.log = logging
		self.log.critical("NikeSpider STARTED.")
		self.date = datetime.today().strftime('%Y-%m-%d')

	def start_requests(self):
		yield SplashRequest(niceKicksUrl, self.parse, args={'wait': 1}, splash_headers={'Authorization': basic_auth_header(APIKEY, '')})

	def parse(self, response):
		try:
			products = response.xpath('//*[@id="shopify-section-collection-template"]/div/main/div/ul[1]/li')
			for product in products:
				item = NiceKicksItem()
				# print(product.xpath('div/div/a/div/img[1]/@data-src').extract())
				item['name'] = product.xpath('div/figure/a[2]/span/h2/text()').extract_first()
				item['price'] = product.xpath('div/figure/a[2]/span/p/span/text()').extract_first()
				item['image'] = "https:" + product.xpath('div/figure/img/@src').extract_first()
				item['link'] = "https://shopnicekicks.com" + product.xpath('div/figure/a[2]/@href').extract_first()
				item['date'] = self.date
				item['colors'] = ""
				yield item
		except Exception as err:
			print(err)

	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(NiceKicksSpider, cls).from_crawler(crawler, *args, **kwargs)
		crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
		return spider

	def spider_closed(self, spider):
		pprint(niceKicksSlackContainer)
		res = niceKicksSlackContainer.send()
		if res:
			self.log.info(res.status_code)
			self.log.info(res.text)
		spider.logger.info('Spider closed: %s', spider.name)
