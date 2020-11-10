#Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json

import requests
import json
from getpass import getpass
username = 'OlgaNP'
password = getpass()

repos = requests.get('https://api.github.com/user/repos', auth=(username, password))

with open('data.json()', 'w', encoding='utf-8') as outfile:
    json.dump(repos.json(),outfile)

for repo in repos.json():
    print(repo['name'])