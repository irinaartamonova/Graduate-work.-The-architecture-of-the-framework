import logging

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils import read_config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Чтение файла конфигурации
config = read_config('Настройки окружения.ini')

# что бы при запуске через консоль не выдавало ошибку
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")  # Добавление аргумента для отключения Sandbox

# Получение BASE_URL и PROFILE_URL из секции ui_config
BASE_URL = config['ui_config']['BASE_URL']
PROFILE_URL = config['ui_config']['PROFILE_URL']


@pytest.mark.ui
def test_find_wrong_book_by_name(driver):
    driver.get(BASE_URL)
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.NAME, "phrase"))
    ).send_keys("3pidjsklfjlsf")
    # нажимаем на кнопку поиска (лупа)
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div/header/div/div[1]/div[2]/div[1]/form/button").click()
    # книгу не нашли
    # 8 сек просто что бы посмотреть
    WebDriverWait(driver, 8).until(lambda d: False)
    logging.info("UI тест поиск несуществующей книги успешно завершен")