from scrapy import Spider, signals
from ..items import AddictItem
from datetime import datetime
from notify.slack import Slack
from config import APIKEY
from scrapy_splash import SplashRequest
from w3lib.http import basic_auth_header
from pprint import pprint
import logging


addictUrl = "https://www.addictmiami.com/collections/latest-products?sort_by=created-descending"
addictSlackContainer = Slack()
addictSlackContainer.add_data("text", "*Now and upcoming stock on AddictMiami* :tada::tada:")


class AddictSpider(Spider):
	name = "addict"
	allowed_domains = ["addictmiami.com"]
	start_urls = [addictUrl]

	def __init__(self):
		super(AddictSpider, self).__init__()
		self.log = logging
		self.log.critical("NikeSpider STARTED.")
		self.date = datetime.today().strftime('%Y-%m-%d')

	def start_requests(self):
		yield SplashRequest(addictUrl, self.parse, args={'wait': 1}, splash_headers={'Authorization': basic_auth_header(APIKEY, '')})

	def parse(self, response):
		try:
			products = response.xpath('//*[@id="MainContent"]/div/div[1]/div')
			for product in products:
				item = AddictItem()
				# print(product.xpath('div/div/a/div/img[1]/@data-src').extract())
				item['name'] = product.xpath('a/div[2]/div[1]/text()').extract_first()
				item['price'] = product.xpath('a/div[2]/div[2]/span/text()').extract_first()
				item['image'] = "https:" + product.xpath('a/div[1]/img/@src').extract_first()
				item['link'] = "https://www.addictmiami.com" + product.xpath('a/@href').extract_first()
				item['date'] = self.date
				item['colors'] = ""
				yield item
		except Exception as err:
			print(err)

	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(AddictSpider, cls).from_crawler(crawler, *args, **kwargs)
		crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
		return spider

	def spider_closed(self, spider):
		pprint(addictSlackContainer)
		res = addictSlackContainer.send()
		if res:
			self.log.info(res.status_code)
			self.log.info(res.text)
		spider.logger.info('Spider closed: %s', spider.name)
