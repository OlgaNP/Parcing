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

main_link = 'https://yandex.ru/news/rubric/culture'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

response = requests.get(main_link,headers=headers)
dom = html.fromstring(response.text)

items = dom.xpath("//a[contains(@href, 'culture') and @class = 'news-card__link']/ancestor::article")

news_list = []
for item in items:
    news = {}
    news_name = item.xpath(".//a[contains(@href, 'culture') and @class = 'news-card__link']/h2/text()")
    news_sourse = item.xpath(".//span[@class = 'mg-card-source__source']/a/text()")
    news_link = item.xpath(".//a[contains(@href, 'culture') and @class = 'news-card__link']/@href")
    news_date = item.xpath(".//span[@class = 'mg-card-source__time']/text()")
    news['name'] = news_name[0]
    news['sourse'] = news_sourse[0]
    news['link'] = news_link[0]
    news['date'] = news_date[0]
    news_list.append(news)


pprint(news_list)
client = MongoClient('127.0.0.1', 27017)
db = client['yandex_news']
yandex_collection = db.yandex_collection
yandex_collection.insert_many(news_list)

