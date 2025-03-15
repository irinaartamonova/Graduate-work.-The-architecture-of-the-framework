import configparser
import logging

import pytest
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Чтение файла конфигурации
config1 = configparser.ConfigParser()
config1.read('настройки окружения.ini')

config2 = configparser.ConfigParser(interpolation=None)
config2.read("тестовые данные.ini")

# Получение BASE_URL из секции api_config
BASE_URL = config1['api_config']['BASE_URL']

headers = {
    "Cookie": config2["headers"]["cookie"],
    "User-Agent": config2["headers"]["user-agent"],
    "Referer": config2["headers"]["referer"],
    "Authorization": config2["headers"]["authorization"]
}

# поменяла id книги с главной которая уже есть в корзине потому что книги с таким id нет на главной или на сайте(наверно)
# поменяла id книги которой нет складе потому что она есть на складе
test_cases = [
    ("Добавить книгу, которая уже в корзине",
     {
         "id": 3082934, "adData":
         {
             "item_list_name": "index", "product_shelf": "Новинки литературы"
         }
     }, 200),
]

@pytest.mark.api
@pytest.mark.parametrize("test_name, payload, expected_status", test_cases)
def test_cart_operations(test_name, payload, expected_status):
    response = requests.post(BASE_URL, json=payload, headers=headers)
    assert response.status_code == expected_status, f"{test_name} - Ожидаемый статус {expected_status}, полученный статус {response.status_code}"
    logging.info("API тест успешно завершен")
    pass