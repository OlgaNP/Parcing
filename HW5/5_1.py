# 1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах в базу данных
# (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172
#

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint
from pymongo import MongoClient

chrome_options = Options()
driver = webdriver.Chrome()
driver.get('https://mail.ru/')

elem = driver.find_element_by_id('mailbox:login-input')
elem.send_keys('study.ai_172')
elem.send_keys(Keys.ENTER)
time.sleep(3)
elem = driver.find_element_by_id('mailbox:password-input')
elem.send_keys('NextPassword172')
elem.send_keys(Keys.ENTER)

driver.get('https://e.mail.ru/inbox')
links = set()

while True:
    letter_list = len(links)
    time.sleep(3)
    scroll = ActionChains(driver)
    letters = driver.find_elements_by_class_name('js-letter-list-item')
    for letter in letters:
        links.add(letter.get_attribute('href'))
    letter_listnew = len(links)
    if letter_list == letter_listnew:
        break
    scroll.move_to_element(letters[-1])
    scroll.perform()

letters_info = []
for link in links:
    letter = {}
    driver.get(link)
    time.sleep(5)
    sender = driver.find_element_by_class_name('letter-contact').text
    send_date = driver.find_element_by_class_name('letter__date').text
    subject = driver.find_element_by_class_name('thread__subject').text
    try:
        letter_text = driver.find_element_by_class_name('js-helper').text
    except:
        text = "Nonreadable"

    letter['Тема письма'] = subject
    letter['Текст письма'] = letter_text
    letter['Отправитель'] = sender
    letter['Дата отправки'] = send_date

    letters_info.append(letter)

pprint(letters_info)
driver.quit()

client = MongoClient('127.0.0.1', 27017)
db = client['letters_mail_ru']
letters_collection = db.letters_collection
letters_collection.insert_many(letters_info)





















# 2) Написать программу, которая собирает «Хиты продаж» с сайта техники mvideo и складывает данные в БД. Магазины можно выбрать свои.
# Главный критерий выбора: динамически загружаемые товары