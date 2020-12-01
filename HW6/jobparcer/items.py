# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class JobparcerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item_name = scrapy.Field()
    item_salary = scrapy.Field()
    _id = scrapy.Field()
    item_source = scrapy.Field()
    item_link = scrapy.Field()
