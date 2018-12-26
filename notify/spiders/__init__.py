# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from .kith import KithSpider
from .nike import NikeSpider
from .yeezy import YeezySpider
from .adidas import AdidasSpider

__all__ = ["KithSpider", "NikeSpider", "YeezySpider", "AdidasSpider"]
