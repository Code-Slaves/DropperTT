import bcrypt
import requests
import json

# Ваш базовый URL. Замените его на URL вашего сервера.
BASE_URL = 'https://cryptonx.org/update'

# Ваш секретный пароль
password = 'D12345678'

# Создайте хеш вашего пароля
password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 

#СМЕНА ССЫЛКИ
# Новый URL, который вы хотите установить для редиректа
new_url = 'https://nolewex.com/'

# Подготовьте заголовки и тело запроса
headers = {
    'Content-Type': 'application/json'
}

payload = {
    'password': password_hash,  # отправляем хеш пароля, а не сам пароль
    'newUrl': new_url
}


# BASE_URL = 'https://cryptonx.org/statistic'

# #СТАТИСТИКА
# # Данные для отправки в теле запроса
# payload = {
#     'password': password_hash,  # замените на ваш настоящий пароль
#     'startDate': '2023-10-24',  # пример даты, замените на вашу реальную дату
#     'endDate': '2023-10-30'  # пример даты, замените на вашу реальную дату
# }

# # Дополнительные заголовки (если это необходимо для вашего сервера)
# headers = {
#     'Content-Type': 'application/json'
# }


# Отправьте POST-запрос
response = requests.post(BASE_URL, json=payload, headers=headers)

# Выведите ответ сервера
print(response.text)
