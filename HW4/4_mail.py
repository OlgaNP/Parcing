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

#выбирались новости из блока Политика

main_link = 'https://news.mail.ru'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}

response = requests.get(main_link, headers=headers)
dom = html.fromstring(response.text)

links = dom.xpath(".//a[contains(@href, 'politics') and @class = 'newsitem__title link-holder']/@href|.//a[contains(@href, 'politics') and @class = 'link link_flex']/@href")

news_list = []
for link in links:
    main_link = link
    response = requests.get(main_link, headers=headers)
    dom = html.fromstring(response.text)
    news = {}

    news_name = dom.xpath("//h1[@class='hdr__inner']/text()")
    news_date = dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")
    news_sourse = dom.xpath("//a[@class='link color_gray breadcrumbs__link']/span[@class='link__text']/text()")

    news['source'] = news_sourse
    news['name'] = news_name[0]
    news['link'] = main_link
    news['date'] = news_date[0].split('T')[0]
    news_list.append(news)

pprint(news_list)
client = MongoClient('127.0.0.1', 27017)
db = client['mail_news']
mail_collection = db.mail_collection
mail_collection.insert_many(news_list)


