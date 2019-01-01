from scrapy import Spider, signals, Request
from ..items import RiseItem
from datetime import datetime
from notify.slack import Slack
from config import APIKEY
from scrapy_splash import SplashRequest
from w3lib.http import basic_auth_header
from pprint import pprint
import logging


riseUrl = "https://rise45.com/collections/rise-new-arrivals/?sort_by=created-descending"
riseSlackContainer = Slack()
riseSlackContainer.add_data("text", "*Now and upcoming stock on Rise45* :tada::tada:")


class RiseSpider(Spider):
	name = "rise"
	allowed_domains = ["rise45.com"]
	start_urls = [riseUrl]

	def __init__(self):
		super(RiseSpider, self).__init__()
		self.log = logging
		self.log.critical("NikeSpider STARTED.")
		self.date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

	def start_requests(self):
		yield SplashRequest(riseUrl, self.parse, args={'wait': 3}, splash_headers={'Authorization': basic_auth_header(APIKEY, '')})

	def parse(self, response):
		try:
			products = response.xpath('//*[@id="shopify-section-collection-template"]/section/div[3]/div[2]/div/div[1]/div/div')
			# pprint(products)
			for product in products:
				item = RiseItem()
				# print(product.xpath('div/div/a/div/img[1]/@data-src').extract())
				item['name'] = product.xpath('div/div/div/h2/a/text()').extract_first()
				item['price'] = product.xpath('div/div/div/div/span/text()').extract_first()
				item['image'] = "https:" + product.xpath('div/div/a/div/img[1]/@data-src').extract_first().replace('{width}', '400')
				item['link'] = "https://rise45.com" + product.xpath('div/div/div/h2/a/@href').extract_first()
				item['date'] = self.date
				item['colors'] = ""
				yield item
		except Exception as err:
			print(err)

	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(RiseSpider, cls).from_crawler(crawler, *args, **kwargs)
		crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
		return spider

	def spider_closed(self, spider):
		pprint(riseSlackContainer)
		res = riseSlackContainer.send()
		if res:
			self.log.info(res.status_code)
			self.log.info(res.text)
		spider.logger.info('Spider closed: %s', spider.name)
