from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from notify.spiders import KithSpider
from notify.spiders import NikeSpider
from notify.spiders import YeezySpider
from notify.spiders import RiseSpider
from notify.spiders import AddictSpider
from notify.spiders import NiceKicksSpider
from notify.spiders import AdidasSpider
import logging


# disable some logs and all that.
logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('scrapy').propagate = False


# CONFIGURE THE SCRAPY CRAWLER RUNNER SO...
runner = CrawlerRunner(get_project_settings())
# runner.crawl(AdidasSpider)
runner.crawl(NikeSpider)
runner.crawl(KithSpider)
runner.crawl(YeezySpider)
runner.crawl(RiseSpider)
runner.crawl(AddictSpider)
runner.crawl(NiceKicksSpider)

# join all of them to run separately
job = runner.join()

# when spiders are done running, stop the reactor...
job.addBoth(lambda _: reactor.stop())

# start the crawling process now then.
reactor.run()
