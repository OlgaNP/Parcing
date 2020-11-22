

from pymongo import MongoClient
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import requests
from pprint import pprint



def hh_search(search_vacancy):
    main_link = 'https://hh.ru'
    params = {'text': search_vacancy, 'page': ''}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
    response = requests.get(main_link + '/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=',
                            params=params, headers=headers)

    vacancy_data = []

    if response.status_code == 200:
        dom = bs(response.text, 'lxml')

        page_block = dom.find('div', {'data-qa': 'pager-block'})
        if not page_block:
            last_page = '1'
        else:
            last_page = int(page_block.find_all('a', {'class': 'HH-Pager-Control'})[-2].getText())

    for page in range(0, last_page):
        params['page'] = page
        response = requests.get(main_link + '/search/vacancy?area=1&fromSearchLine=true&st=searchVacancy&text=',
                                params=params, headers=headers)

        if response.status_code == 200:
            dom = bs(response.text, 'lxml')

            vacancy_items = dom.find_all('div', {'data-qa': 'vacancy-serp__vacancy'})

            for item in vacancy_items:
                vacancy_data.append(get_vacancy_data(item))
    return vacancy_data


def get_vacancy_data(item):
    vacancy_data = {}

    name_vacancy = item.find('span', {'class': 'g-user-content'}).getText()
    vacancy_data['name_vacancy'] = name_vacancy

    get_link = item.find('span', {'class': 'g-user-content'})
    vacancy_link = get_link.findChild()['href']
    vacancy_data['vacancy_link'] = vacancy_link

    company_name = item.find('div', {'class': 'vacancy-serp-item__meta-info'}).getText()
    vacancy_data['company_name'] = company_name

    vacancy_city = item.find('span', {'class': 'vacancy-serp-item__meta-info'}).getText().split(', ')[0].replace(
        u'\xa0', u'')
    vacancy_data['vacancy_city'] = vacancy_city

    salary = item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
    if not salary:
        salary_min = None
        salary_max = None
        salary_currency = None
    else:
        salary = salary.getText().replace('\xa0', '')
        salary = re.split(' |-', salary)

        try:
            salary_currency = salary[2]
        except IndexError:
            salary_currency = salary[1]
        if salary[0] == 'до':
            salary_min = None
            salary_max = int(salary[1])
        elif salary[0] == 'от':
            salary_min = int(salary[1])
            salary_max = None
        else:
            salary_min = int(salary[0])
            try:
                salary_max = int(salary[1])
            except ValueError:
                salary_max = None

    vacancy_data['salary_min'] = salary_min
    vacancy_data['salary_max'] = salary_max
    vacancy_data['salary_currency'] = salary_currency

    return vacancy_data


def parser_vacancy(vacancy_search):
    vacancy_data = []
    vacancy_data.extend(hh_search(vacancy_search))

    vacancy_base = vacancy_data
    return vacancy_base


vacancy_base_hh = parser_vacancy('python')



#1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую
# собранные вакансии в созданную БД.

def write_to_db(vacancy_base_hh):
    client = MongoClient('127.0.0.1', 27017)
    db = client['hh_vacancies']
    vacancies_collection = db.vacancies_collection
    vacancies_collection.insert_many(vacancy_base_hh)
    return vacancies_collection

#write_to_db(vacancy_base_hh)

#функция отработала(к дз приложен скриншот)


#2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.

salary_level = 200000
client = MongoClient('127.0.0.1', 27017)
db = client['hh_vacancies']
vacancies_collection = db.vacancies_collection
for vacancy in vacancies_collection.find({'$or':[{'salary_min':{'$gt':salary_level}},{'salary_max':{'$gt':salary_level}}]}):
    pprint(vacancy)


#3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.

vacancy_data = hh_search('python')
for vacancy in vacancy_data:
    doc = vacancies_collection.find({'vacancy_link': vacancy['vacancy_link']})
    if not doc:
        vacancies_collection.insert_one({'name_vacancy':vacancy['name_vacancy'],'vacancy_link':vacancy['vacancy_link'],'vacancy_city':vacancy['vacancy_city'] , 'company_name' : vacancy['company_name'], 'salary_min':vacancy['salary_min'],'salary_max':vacancy['salary_max'],'salary_currency':vacancy['salary_currency']})
        print(f'Добавлена новая вакансия')
    else:
        print(f'Новых вакансий нет')



