import logging
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from utils import get_config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Чтение файла конфигурации
config = get_config('Настройки окружения.ini')

# что бы при запуске через консоль не выдавало ошибку
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")  # Добавление аргумента для отключения Sandbox

# Получение BASE_URL из секции api_config
BASE_URL = config['ui_config']['BASE_URL']

@pytest.mark.ui
def test_find_book_by_author(driver):
    driver.get(BASE_URL)
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.NAME, "phrase"))
    ).send_keys("Екатерина Вильмонт")
    # нажимаем на кнопку поиска (лупа)
    driver.find_element(By.XPATH, "/html/body/div[2]/div/div/header/div/div[1]/div[2]/div[1]/form/button").click()
    # нашли книгу по автору
    # 8 сек просто что бы посмотреть
    WebDriverWait(driver, 8).until(lambda d: False)
    logging.info("UI тест поиск книги по автору успешно завершен")