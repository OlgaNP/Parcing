from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from instaparcer import settings
from instaparcer.spiders.InstaSpider import InstaspiderSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstaspiderSpider)

    process.start()