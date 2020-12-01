from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparcer.spiders.hhru import HhruSpider
from jobparcer.spiders.superjob import SuperJobSpider
from jobparcer import settings

if __name__ == 'main':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhruSpider)
    process.crawl(SuperJobSpider)
    process.start()