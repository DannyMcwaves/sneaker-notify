# -*- coding: utf-8 -*-
from scrapy import Spider, signals
from notify.slack import Slack
from pprint import pprint
from scrapy_splash import SplashRequest
import logging


__all__ = ["AdidasSpider", "adidasSlackContainer"]


adidasSlackContainer = Slack()
adidasSlackContainer.add_data("text", "*Now and upcoming stock on Nike* :tada::tada:")
adidasUrl = 'https://www.adidas.com/us/men-athletic_sneakers-shoes'


class AdidasSpider(Spider):
	name = 'adidas'
	allowed_domains = ['www.adidas.com']

	def __init__(self):
		super(AdidasSpider, self).__init__()
		self.log = logging
		self.log.critical("Adidas STARTED.")

	def start_requests(self):
		yield SplashRequest(adidasUrl, self.parse, args={'wait': 1})

	def parse(self, response):
		self.log.info(response.body)

	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(AdidasSpider, cls).from_crawler(crawler, *args, **kwargs)
		crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
		return spider

	def spider_closed(self, spider):
		pprint(adidasSlackContainer)
		# res = adidasSlackContainer.send()
		# self.log.info(res.status_code)
		# self.log.info(res.text)
		spider.logger.info('Spider closed: %s', spider.name)
