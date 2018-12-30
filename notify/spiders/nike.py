from scrapy import Spider, signals, Request
from datetime import datetime
from ..items import NikeItem
from notify.slack import Slack
from pprint import pprint
import json
import logging


__all__ = ["NikeSpider", "nikeSlackContainer"]


NikeURL = "https://kith.com/collections/footwear/sneaker?page=1&sort_by=created-descending"
nikeSlackContainer = Slack()
nikeSlackContainer.add_data("text", "*Now and upcoming stock on Nike* :tada::tada:")


class NikeSpider(Spider):
	name = "nike"
	allowed_domains = ["api.nike.com", "nike.com"]
	start_urls = [NikeURL]

	def __init__(self):
		super(NikeSpider, self).__init__()
		self.log = logging
		self.log.critical("NikeSpider STARTED.")
		self.date = datetime.today().strftime('%Y-%m-%d')

	def start_requests(self):
		main_url = 'https://api.nike.com/product_feed/threads/v2/?anchor=0&count=50&filter=marketplace%28US%29&' \
				'filter=language%28en%29&filter=upcoming%28true%29&filter=channelId%28010794e5-35fe-4e32-aaff-cd2c74f89' \
				'd61%29&filter=exclusiveAccess%28true%2Cfalse%29&sort=effectiveStartSellDateAsc&fields=' \
				'active&fields=id&fields=lastFetchTime&fields=productInfo&fields=publishedContent.nodes&fields=' \
				'publishedContent.properties.coverCard&fields=publishedContent.properties.productCard&fields' \
				'=publishedContent.properties.products&fields=publishedContent.properties.publish.collections&fields' \
				'=publishedContent.properties.relatedThreads&fields=publishedContent.properties.seo&fields=' \
				'publishedContent.properties.threadType&fields=publishedContent.properties.custom'
		headers = {
			"Accept": "application/json",
			"Referer": "https://www.nike.com/launch/",
			"Connection": "keep-alive",
			"Accept-Encoding": "gzip, deflate, sdch",
			"Authorization": "Bearer " + " "
		}

		yield Request(main_url, headers=headers, callback=self.parse)

	def parse(self, response):
		try:
			data = json.loads(response.text)['objects']
			for product in data:
				if product['productInfo'][0]['merchProduct']['productType'] == 'FOOTWEAR' and\
						product['productInfo'][0]['merchProduct']['commercePublishDate'].split('T')[0] >= self.date:
					item = NikeItem()
					item["name"] = product['publishedContent']['properties']['seo']['title']
					item["link"] = "https://www.nike.com/launch/t/{}/".format(product['publishedContent']['properties']['seo']['slug']),
					item["image"] = product['productInfo'][0]['imageUrls']['productImageUrl']
					item["releaseType"] = product['productInfo'][0]['launchView']['method']
					item["releaseStart"] = product['productInfo'][0]['launchView']['startEntryDate']
					item["id"] = product['productInfo'][0]['merchProduct']['id']
					item["currentPrice"] = product['productInfo'][0]['merchPrice']['currentPrice']
					item["country"] = product['productInfo'][0]['merchPrice']['country']
					item["sizes"] = [x['nikeSize'] for x in product['productInfo'][0]['skus']]
					item["colors"] = [x['name'] for x in product['productInfo'][0]['productContent']['colors']]
					item["currency"] = product['productInfo'][0]['merchPrice']['currency']
					item["discounted"] = product['productInfo'][0]['merchPrice']['discounted']
					item["fullPrice"] = product['productInfo'][0]['merchPrice']['fullPrice']
					item["genders"] = product['productInfo'][0]['merchProduct']['genders']
					item["date"] = self.date

					yield item

		except Exception as err:
			print(err)
			pass

	@classmethod
	def from_crawler(cls, crawler, *args, **kwargs):
		spider = super(NikeSpider, cls).from_crawler(crawler, *args, **kwargs)
		crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
		return spider

	def spider_closed(self, spider):
		# this is the part where I get to send the data to slack
		pprint(nikeSlackContainer)
		res = nikeSlackContainer.send()
		if res:
			self.log.info(res.status_code)
			self.log.info(res.text)
		spider.logger.info('Spider closed: %s', spider.name)
