from scrapy import Spider, signals, Request
from ..items import NordstromItem
from datetime import datetime
from notify.slack import Slack
from config import APIKEY
from scrapy_splash import SplashRequest
from w3lib.http import basic_auth_header
from pprint import pprint
import logging


nordstromUrl = "https://shop.nordstrom.com/content/sneaker-releases?campaign=0102sneakercalendarhp&cid=k06g6&cm_sp=merch-_-corp_7785_j009163-_-hp_corp_p15_details&jid=j009163-7785"
nordstromSlackContainer = Slack()
nordstromSlackContainer.add_data("text", "*Now and upcoming stock on Rise45* :tada::tada:")


class NordstromSpider(Spider):
	name = "nordstrom"
	allowed_domains = [""]

	def __init__(self):
		super(NordstromSpider, self).__init__()
		self.log = logging
		self.log.critical("NikeSpider STARTED.")
		self.date = datetime.today().strftime('%Y-%m-%d')

	def start_requests(self):
		yield SplashRequest(nordstromUrl, self.parse, args={'wait': 5}, splash_headers={'Authorization': basic_auth_header(APIKEY, '')})

	def parse(self, response):
		try:
			products = response.xpath('//*[@id="root"]/div/div[1]/div/div[2]/div[1]/section/div/div/main/div/div/div')
			# pprint(products)
			for product in products:
				item = NordstromItem()
				# print(product.xpath('div/div/div[1]/section/div/div/div/img').extract())
				# print(product.xpath('div/div/div[3]/section/div/h4/p').extract())
				item['name'] = product.xpath('div/div/div[3]/section/div/h4/p').extract_first()
				# item['price'] = product.xpath('div/div/div/div/span/text()').extract_first()
				# item['image'] = "https:" + product.xpath('div/div/a/div/img[1]/@data-src').extract_first().replace('{width}', '400')
				# item['link'] = "https://rise45.com" + product.xpath('div/div/div/h2/a/@href').extract_first()
				# item['date'] = self.date
				# item['colors'] = ""
				yield item
		except Exception as err:
			print(err)

	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(NordstromSpider, cls).from_crawler(crawler, *args, **kwargs)
		crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
		return spider

	def spider_closed(self, spider):
		pprint(nordstromSlackContainer)
		res = nordstromSlackContainer.send()
		if res:
			self.log.info(res.status_code)
			self.log.info(res.text)
		spider.logger.info('Spider closed: %s', spider.name)
