#2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД.
# Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import time
from pprint import pprint


chrome_options = Options()

chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)
driver.get('https://www.mvideo.ru/')

links = []
mvideo_goods =[]

scroll = driver.find_element_by_xpath("//div[contains(text(), 'Хиты продаж')]/../../../..//a[contains(@class, 'next-btn')]")


while True:
    time.sleep(5)
    len1 = len(links)
    hits = driver.find_elements_by_xpath("//div[contains(text(), 'Хиты продаж')]/../../../..//a[contains(@class, 'sel-product-tile-title')]")
    goods = {}
    for hit in hits:
        link = hit.get_attribute('href')
        if link not in links:
            links.append(link)
            goods = {'data': hit.get_attribute("data-product-info")}
            mvideo_goods.append(goods)
        else:
            pass

    len2 = len(links)
    if len1 != len2:
        scroll.click()
    else:
        break


pprint(mvideo_goods)
driver.quit()


client = MongoClient('127.0.0.1', 27017)
db = client['mvideo_goods']
mvideo_collection = db.mvideo_collection
mvideo_collection.insert_many(mvideo_goods)