# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


__all__ = ["KithItem", "NikeItem", "YeezyItem", 'AdidasItem']


class KithItem(Item):
    date = Field()
    price = Field()
    image = Field()
    link = Field()
    name = Field()
    size = Field()
    sizes = Field()
    colors = Field()


class AdidasItem(Item):
    date = Field()
    price = Field()
    image = Field()
    link = Field()
    name = Field()
    size = Field()
    sizes = Field()
    colors = Field()


class YeezyItem(Item):
    date = Field()
    price = Field()
    image = Field()
    link = Field()
    name = Field()
    size = Field()
    sizes = Field()
    colors = Field()


class NikeItem(Item):
    date = Field()
    currentPrice = Field()
    fullPrice = Field()
    discounted = Field()
    image = Field()
    link = Field()
    name = Field()
    currency = Field()
    country = Field()
    sizes = Field()
    genders = Field()
    id = Field()
    releaseType = Field()
    releaseStart = Field()
    colors = Field()
