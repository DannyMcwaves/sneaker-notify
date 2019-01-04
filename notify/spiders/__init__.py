# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from .kith import KithSpider
from .nike import NikeSpider
from .yeezy import YeezySpider
from .adidas import AdidasSpider
from .rise import RiseSpider
from .addict import AddictSpider
from .nice_kicks import NiceKicksSpider
from .nordstrom import NordstromSpider

__all__ = [
	"KithSpider", "NikeSpider", "YeezySpider", "AdidasSpider",
	"RiseSpider", "AddictSpider", "NiceKicksSpider", "NordstromSpider"]
