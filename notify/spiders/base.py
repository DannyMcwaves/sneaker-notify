from scrapy import Spider, signals, Request
from ..items import BaseItem
from datetime import datetime
from notify.slack import Slack
from config import APIKEY
from scrapy_splash import SplashRequest
from w3lib.http import basic_auth_header
from pprint import pprint
import logging


Url = ""
SlackContainer = Slack()
SlackContainer.add_data("text", "*Now and upcoming stock on Rise45* :tada::tada:")


class RiseSpider(Spider):
	name = "base"
	allowed_domains = [""]
	start_urls = [Url]

	def __init__(self):
		super(RiseSpider, self).__init__()
		self.log = logging
		self.log.critical("NikeSpider STARTED.")
		self.date = datetime.today().strftime('%Y-%m-%d')

	def start_requests(self):
		yield SplashRequest(Url, self.parse, args={'wait': 1}, splash_headers={'Authorization': basic_auth_header(APIKEY, '')})

	def parse(self, response):
		pprint(response)
		return response

	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(RiseSpider, cls).from_crawler(crawler, *args, **kwargs)
		crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
		return spider

	def spider_closed(self, spider):
		pprint(SlackContainer)
		res = SlackContainer.send()
		if res:
			self.log.info(res.status_code)
			self.log.info(res.text)
		spider.logger.info('Spider closed: %s', spider.name)
