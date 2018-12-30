# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from .items import KithItem, NikeItem, YeezyItem, AdidasItem
from notify.util import insert_data, create_tables
from config import KITH_CONTAINER, NIKE_CONTAINER, YEEZY_CONTAINER, ADIDAS_CONTAINER
from .spiders.kith import kithSlackContainer
from .spiders.nike import nikeSlackContainer
from .spiders.yeezy import yeezySlackContainer


# start creating the tables.
create_tables()


class SnkrsNotifyPipeline(object):

	def __init__(self):
		"""this is the initiation of the pipeline sequence"""

	def process_item(self, item, spider):

		# check for kith shoes
		if isinstance(item, KithItem):
			data = item
			res = insert_data('kith', name=str(data['name']), price=data['price'], image=data['image'], link=data['link'], date=data['date'])
			print(res)
			if res == 'Done':
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
			res = insert_data('nike', name=str(data['name']), price=data['fullPrice'], image=data['image'], link=data['link'], date=data['date'])
			print(res)
			if res == 'Done':
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
			res = insert_data('yeezy', name=str(data['name']), price=data['price'], image=data['image'], link=data['link'], date=data['date'])
			print(res)
			if res == 'Done':
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
			res = insert_data('yeezy', name=str(data['name']), price=data['price'], image=data['image'], link=data['link'], date=data['date'])
			print(res)
			if res == 'Done':
				print(data)

		return item
