# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import KithItem, NikeItem, YeezyItem, AdidasItem, RiseItem, AddictItem, NiceKicksItem, NordstromItem
from notify.util import SQLite, Redis
from .spiders.kith import kithSlackContainer
from .spiders.nike import nikeSlackContainer
from .spiders.yeezy import yeezySlackContainer
from .spiders.rise import riseSlackContainer
from .spiders.nice_kicks import niceKicksSlackContainer
from .spiders.addict import addictSlackContainer


# start creating the tables.
# sqlite = SQLite()
# sqlite.create_tables()
redis = Redis()


class SnkrsNotifyPipeline(object):

	def __init__(self):
		"""this is the initiation of the pipeline sequence. """

	def process_item(self, item, spider):

		# check for kith shoes
		if isinstance(item, KithItem):
			data = item
			res = redis.add('kith', data)
			print(res)
			if res:
				both = zip(data['size'], data["sizes"])
				size = "\n".join(["<{}|{}>".format(x[0], x[1]) for x in both])
				kithSlackContainer.create_attachment({
					"title": "{} - {}".format(data["name"], data["price"]),
					"title_link": data["link"],
					"fallbacK": "{} - {}".format(data["name"], data["price"]),
					"author_name": "kith",
					"author_link": "https://kith.com/",
					"author_icon": "https://cdn.shopify.com/s/files/1/0094/2252/t/131/assets/logo.png?6931257255964580709",
					"thumb_url": "https://cdn.shopify.com/s/files/1/0094/2252/t/131/assets/logo.png?6931257255964580709",
					"text": "*price*: {} \n *sizes*: {} \n *colors*: {}".format(data["price"], size, data["colors"]),
					"image_url": data["image"],
					"color": "#cc00cc"
				})

		# check for nike shoes.
		if isinstance(item, NikeItem):
			data = item
			res = redis.add('nike', data)
			print(res)
			if res:
				nikeSlackContainer.create_attachment({
					"title": data["name"],
					"title_link": data["link"][0],
					"fallback": "{} - {}".format(data["name"], data["fullPrice"]),
					"author_name": "Nike",
					"author_link": "http://www.nike.com/us/en_us",
					"image_url": data["image"],
					"color": "#cc3366",
					"fields": [
						{
							"title": "Price",
							"value": "{} {}".format(data["fullPrice"], data["currency"]),
							"short": "true"
						}, {
							"title": "Discounted",
							"value": str(data["discounted"]),
							"short": "true"
						},
						{
							"title": "Genders",
							"value": " & ".join(data["genders"]),
							"short": "true"
						}, {
							"title": "Release Type",
							"value": "LAUNCH",
							"short": "true"
						}, {
							"title": "Selection Method",
							"value": data["releaseType"],
							"short": "true"
						}, {
							"title": "Release Date",
							"value": data["releaseStart"],
							"short": "true"
						}, {
							"title": "Colors",
							"value": " - ".join(data["colors"]),
							"short": False
						}, {
							"title": "Sizes",
							"value": "\n".join(data['sizes']),
							"short": False
						}
					]
				})

		# check and run yeezy instance
		if isinstance(item, YeezyItem):
			data = item
			res = redis.add('yeezy', data)
			print(res)
			if res:
				yeezySlackContainer.create_attachment({
					"title": data["name"],
					"title_link": data["link"],
					"fallback": "{} - {}".format(data["name"], data["price"]),
					"author_name": "Yeezy Plus",
					"author_link": "https://yeezysupply.com/collections/new-arrivals",
					"image_url": data["image"],
					"color": "#000000",
					"fields": [
						{
							"title": "Price",
							"value": data["price"],
							"short": "true"
						}
					]
				})

		# check for an adidas instance and parse the result
		if isinstance(item, AdidasItem):
			data = item
			res = redis.add('yeezy', data)
			print(res)
			if res:
				print(data)

		if isinstance(item, RiseItem):
			data = item
			res = redis.add('rise', data)
			print(res)
			if res:
				riseSlackContainer.create_attachment({
					"title": data["name"],
					"title_link": data["link"],
					"fallback": "{} - {}".format(data["name"], data["price"]),
					"author_name": "Rise 45",
					"author_link": "https://rise45.com/collections/rise-new-arrivals",
					"image_url": data["image"],
					"color": "#efefef",
					"fields": [
						{
							"title": "Price",
							"value": data["price"],
							"short": "true"
						}
					]
				})

		if isinstance(item, AddictItem):
			data = item
			res = redis.add('addict', data)
			print(res)
			if res:
				addictSlackContainer.create_attachment({
					"title": data["name"],
					"title_link": data["link"],
					"fallback": "{} - {}".format(data["name"], data["price"]),
					"author_name": "Addict Miami",
					"author_link": "https://www.addictmiami.com/collections/latest-products?sort_by=created-descending",
					"image_url": data["image"],
					"color": "#efefef",
					"fields": [
						{
							"title": "Price",
							"value": data["price"],
							"short": "true"
						}
					]
				})

		if isinstance(item, NiceKicksItem):
			data = item
			res = redis.add('nicekicks', data)
			print(res)
			if res:
				niceKicksSlackContainer.create_attachment({
					"title": data["name"],
					"title_link": data["link"],
					"fallback": "{} - {}".format(data["name"], data["price"]),
					"author_name": "Shop Nice Kicks",
					"author_link": "https://shopnicekicks.com/collections/new-arrivals-1",
					"image_url": data["image"],
					"color": "#e8e8e8",
					"fields": [
						{
							"title": "Price",
							"value": data["price"],
							"short": "true"
						}
					]
				})

		if isinstance(item, NordstromItem):
			"""
			"""
			# print(item)

		return item
