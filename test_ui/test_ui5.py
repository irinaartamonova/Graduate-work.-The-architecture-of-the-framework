import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from utils import configure_logging, read_config

configure_logging()  # Настраиваем логирование

config = read_config('Настройки окружения.ini')  # Читаем конфигурацию
BASE_URL = config['ui_config']['BASE_URL']
PROFILE_URL = config['ui_config']['PROFILE_URL']

@pytest.mark.ui
def test_buy_book(driver):
    # get_and_save_headers(driver) #  Удалите эту строку, если `get_and_save_headers` нужно вызывать только один раз
    # запускаем функцию поиска книги
    test_find_right_book_by_name(driver)
    # ищем тег span купить и нажимаем
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH,
                                     "/html/body/div[2]/div/div/div[3]/div[1]/div/div/div[1]/section/section/div/article[1]/div[3]/div/span"))
    ).click()
    # ищем ссылку на корзину и нажимаем
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/header/div/div[2]/a"))
    ).click()
    # смотрим что в корзине
    WebDriverWait(driver, 100).until(lambda d: False)  
    logging.info("UI тест добавление существующей книги в корзину успешно завершен")