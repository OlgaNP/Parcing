from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from leroymerlen import settings
from leroymerlen.spiders.lm import LmSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LmSpider, search='гирлянда')

    process.start()