import logging
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils import read_config,find_element_and_send_keys, click_element 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Чтение файла конфигурации
config = read_config()

# Получение BASE_URL из секции ui_config
BASE_URL = config['ui_config']['BASE_URL']

# что бы при запуске через консоль не выдавало ошибку
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")  # Добавление аргумента для отключения Sandbox

@pytest.mark.ui
def test_find_right_book_by_name(driver):
    # открывается страница
    driver.get(BASE_URL)

    # Находим поле поиска книги по имени и вводим название книги
    find_element_and_send_keys(driver, By.NAME, "phrase", "1984")

    # Нажимаем на кнопку поиска (лупа)
    click_element(driver, By.XPATH, "/html/body/div[2]/div/div/header/div/div[1]/div[2]/div[1]/form/button")

    # 8 сек просто что бы посмотреть (лучше заменить на более надежный способ проверки)
    WebDriverWait(driver, 8).until(lambda d: False)  # Замена time.sleep для просмотра

    logging.info("UI тест поиск существующей книги успешно завершен")