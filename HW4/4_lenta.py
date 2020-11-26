# #Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные данные в БД

from pprint import pprint
from lxml import html
import requests
from pymongo import MongoClient

#выбирались новости из блока Культура

main_link = 'https://lenta.ru'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

response = requests.get(main_link,headers=headers)
dom = html.fromstring(response.text)

items = dom.xpath('//div[@class="span4"]/div[@class="first-item"]/h2/a|//div[@class="span4"]/div[@class="item"]/a')

news_list = []
for item in items:
    news = {}
    news_name = item.xpath(".//time[@class='g-time']/../text()")
    news_sourse = main_link
    news_link = item.xpath(".//time[@class='g-time']/../@href")
    news_date = item.xpath(".//time[@class='g-time']/@datetime")
    news['name'] = news_name[0].replace("\xa0"," ")
    news['sourse'] = news_sourse
    news['link'] = main_link + news_link[0]
    news['date'] = news_date
    news_list.append(news)


pprint(news_list)
client = MongoClient('127.0.0.1', 27017)
db = client['lenta_news']
lenta_collection = db.lenta_collection
lenta_collection.insert_many(news_list)

