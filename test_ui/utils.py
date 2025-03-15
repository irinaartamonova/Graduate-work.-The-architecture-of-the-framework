import configparser
import logging

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def get_config(config_file):
    """Читает конфигурацию из указанного .ini файла."""
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def wait_and_click(driver, locator, timeout=5):
    """Ожидает, пока элемент станет кликабельным, и кликает по нему."""
    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    ).click()

def wait_and_send_keys(driver, locator, keys, timeout=5):
    """Ожидает появления элемента и вводит в него текст."""
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    ).send_keys(keys)

def get_and_save_headers(driver, config_file, PROFILE_URL):
    """Получает и сохраняет заголовки, куки и user_agent в файл."""
    # Получаем все необходимые заголовки из браузера
    driver.get(PROFILE_URL)
    cookie = driver.execute_script("return document.cookie;")
    user_agent = driver.execute_script("return navigator.userAgent;")
    authorization = driver.execute_script("return localStorage.getItem('Authorization');")

    # Если cookie, user_agent или authorization не пустые, записываем их в файл
    if cookie or user_agent or authorization:
        config = configparser.ConfigParser(interpolation=None)  # Отключаем интерполяцию
        config.read(config_file)

        if 'headers' not in config:
            config.add_section('headers')

        if cookie:
            config.set('headers', 'Cookie', cookie)
        if user_agent:
            config.set('headers', 'User-Agent', user_agent)
        if authorization:
            config.set('headers', 'Authorization', authorization)

        with open(config_file, 'w') as configfile:
            config.write(configfile)
            logging.info(f"Заголовки сохранены в файл: {config_file}")  # Добавлено сообщение логирования