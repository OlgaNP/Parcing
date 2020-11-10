#2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое, требующее авторизацию
# (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import json

domain = 'https://api.vk.com/method'

token = 'удалено'
user_id = 406446218
v = '5.52'
fields = 'name'

headers = {
    'Content-Type': 'application/json', \
    'Authorization': token
}

query = f"{domain}/groups.get?access_token={token}&user_id={user_id}&fields={fields}&v={v}&extended=1"
response = requests.get(query, headers=headers)

print(response.json())

with open('response.json', 'w',encoding='utf-8') as f:
    json.dump(response.json(), f)