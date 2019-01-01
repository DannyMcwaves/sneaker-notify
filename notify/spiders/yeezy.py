# -*- coding: utf-8 -*-
from scrapy import Spider, signals
from datetime import datetime
from w3lib.http import basic_auth_header
from ..items import YeezyItem
from notify.slack import Slack
from config import APIKEY
from scrapy_splash import SplashRequest
from pprint import pprint
import logging


__all__ = ["YeezySpider", "yeezySlackContainer"]


yeezySlackContainer = Slack()
yeezySlackContainer.add_data("text", "*New arrivals on Yeezy Supply* :tada::tada:")


class YeezySpider(Spider):
	name = 'yeezy'
	allowed_domains = ['yeezysupply.com']
	start_urls = ['https://yeezysupply.com/collections/new-arrivals-footwear/']

	def __init__(self):
		super(YeezySpider, self).__init__()
		self.log = logging
		self.log.critical("Yeezy STARTED.")
		self.date = datetime.today().strftime('%Y-%m-%d')

	def start_requests(self):
		yield SplashRequest("https://yeezysupply.com/collections/new-arrivals-footwear/", self.parse, args={'wait': 1}, splash_headers={'Authorization': basic_auth_header(APIKEY, '')})

	def parse(self, response):
		try:
			topli = response.xpath('//*[@id="main"]/div[1]/ul/li')
			for product in topli:
				if product.extract() != '<li>':
					item = YeezyItem()
					item['name'] = product.xpath('a/span[2]/text()').extract_first().strip().replace('\xa0', ' ')
					item['price'] = product.xpath('a/span[3]/span/text()').extract_first()
					item['image'] = "https:" + product.xpath('a/span[1]/picture/source[1]/@srcset').extract_first()
					item['link'] = "https://yeezysupply.com" + product.xpath('a/@href').extract_first()
					item['date'] = self.date
					item['colors'] = ''
					yield item
		except Exception as err:
			print(err)
			pass

	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(YeezySpider, cls).from_crawler(crawler, *args, **kwargs)
		crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
		return spider

	def spider_closed(self, spider):
		pprint(yeezySlackContainer)
		res = yeezySlackContainer.send()
		if res:
			self.log.info(res.status_code)
			self.log.info(res.text)
		spider.logger.info('Spider closed: %s', spider.name)
