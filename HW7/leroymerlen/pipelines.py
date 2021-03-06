# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class LeroyMerlenPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroymerlen

    def process_item(self, item, spider):
        item['characteristics'] = dict(zip(item['characteristic_name'], item['characteristic_value']))
        collection = self.mongo_base[spider.name]
        # collection.insert_one(item)
        collection.insert_one({'name': item['name'], 'photos': item['photos'], 'price': item['price'],
                               'currency': item['currency'], 'unit': item['unit'], 'link': item['link'],
                               'characteristics': item['characteristics']})
        return item


class LeroyMerlenPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)
        return item

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        dir = item['name']
        image_guid = request.url.split('/')[-1]
        return f'{dir}/img{image_guid}'

