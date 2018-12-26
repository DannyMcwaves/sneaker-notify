from scrapy import Spider, signals
from w3lib.http import basic_auth_header
from datetime import datetime
from notify.config import APIKEY
from ..items import KithItem
from scrapy_splash import SplashRequest
from notify.slack import Slack
from pprint import pprint
import logging


__all__ = ["KithSpider", "kithSlackContainer"]


KithURL = "https://kith.com/collections/footwear/sneaker?page=1&sort_by=created-descending"
kithSlackContainer = Slack()
kithSlackContainer.add_data("text", "*Now available in stock on Kith* :tada::tada:")


class KithSpider(Spider):
	name = "kith"
	allowed_domains = ["kith.com"]
	start_urls = [KithURL]

	def __init__(self):
		super(KithSpider, self).__init__()
		self.log = logging
		self.log.critical("KithSpider STARTED.")

	def start_requests(self):
		yield SplashRequest(KithURL, self.parse, args={'wait': 1}, splash_headers={'Authorization': basic_auth_header(APIKEY, '')})

	def parser(self, response):
		products = response.xpath('//*[@id="MainContent"]/div/div[1]/div[3]/div[2]/div[2]/div/div[2]/div')
		for p in products:
			pprint(p.extract())
			# img = p.xpath('div/div/div/div/div/a[2]/img').extract_first()

	def parse(self, response):
		try:
			products = response.xpath('//*[@id="MainContent"]/div/div[1]/div[3]/div[2]/div[2]/div/div[2]/div')
			for product in products:
				item = KithItem()
				item['name'] = product.xpath('div/div/a/div/div[1]/div[1]/p[1]/span/text()').extract_first().strip()
				item['price'] = product.xpath('div/div/a/div/div[1]/div[2]/p/text()').extract_first().strip()
				item['colors'] = product.xpath('div/div/a/div/div[1]/div[1]/p[2]/text()').extract_first().strip()
				item['sizes'] = product.xpath('@data-sizes').extract_first().split(',')
				item['link'] = "https://kith.com" + product.xpath('div/div/a/@href').extract_first()
				item['date'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
				item['size'] = ['https://kith.com/cart/add.js?id={}&quantity=1'.format(x.xpath('@data-value').extract_first()) for x in product.xpath('div/div/a/div/div[2]/div')]
				item["image"] = 'https:' + product.xpath('div/div/div/a[1]/img/@src').extract_first()
				yield item

		except Exception as err:
			print(err)
			pass

	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(KithSpider, cls).from_crawler(crawler, *args, **kwargs)
		crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
		return spider

	def spider_closed(self, spider):
		# this is the part where I get to send the data to slack
		pprint(kithSlackContainer)
		res = kithSlackContainer.send()
		self.log.info(res.status_code)
		self.log.info(res.text)
		spider.logger.info('Spider closed: %s', spider.name)
