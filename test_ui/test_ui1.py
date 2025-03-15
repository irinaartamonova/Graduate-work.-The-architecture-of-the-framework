import logging
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Импортируем функции из utils.py
from utils import get_config, wait_and_click, wait_and_send_keys, get_and_save_headers

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Чтение файла конфигурации
config = get_config('Настройки окружения.ini')

# что бы при запуске через консоль не выдавало ошибку
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")  # Добавление аргумента для отключения Sandbox

# Получение BASE_URL и PROFILE_URL из секции ui_config
BASE_URL = config['ui_config']['BASE_URL']
PROFILE_URL = config['ui_config']['PROFILE_URL']

@pytest.fixture(scope="session")
def driver():
    # Запуск браузера хром
    driver = webdriver.Chrome(options=options)  # передаем options сюда
    driver.maximize_window()
    # 10 сек ждем пока запустится
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.ui
def test_registration(driver):
    # открывается страница
    driver.get(BASE_URL)

    # ждем до 5 сек пока браузер прогрузит страницу и кнопка "Войти" станет кликабельной и нажимаем
    wait_and_click(driver, (By.CLASS_NAME, "header-profile__button"))

    # находим input тег с вводом телефона по имени тега
    wait_and_send_keys(driver, (By.NAME, "phone"), "+914080686")

    # находим кнопку "Получить код" по полному пути до этого тега(по имени класса не работала)
    wait_and_click(driver, (By.XPATH,
                                     "/html/body/div[2]/div/div/div[5]/div/div[2]/div/div[2]/div/div[1]/div/form/button"))

    # Ожидаем появления элемента для ввода кода, чтобы убедиться, что страница загрузилась
    EC.presence_of_element_located((By.XPATH,
                                         "/html/body/div[2]/div/div/div[5]/div/div[2]/div/div[2]/div/div[1]/div/form/div[3]/label/input"))

    # есть 60 сек пока придет код на телефон и введем его в поле
    # Проверяем, если после ввода кода произошло перенаправление на главную страницу
    # значит уже зарегистрированный номер тогда обновление заголовков
    if driver.current_url == BASE_URL:
        # если редирект на главную страницу — регистрация завершена
        # заполняем или перезаполняем в файл тестовые данные.ini медвежий токен, куки, user_agent и все
        # что бы использовать в api тестах
        get_and_save_headers(driver, 'тестовые данные.ini', PROFILE_URL)
        logging.info("UI тест регистрация успешно завершен")
    else:
        # Если редиректа не произошло, продолжаем регистрацию и заполняем тестовые данные.ini
        # вводим в поле с именем имя
        wait_and_send_keys(driver, (By.XPATH,
                                             "/html/body/div[2]/div/div/div[5]/div/div[2]/div/div[2]/div/div[1]/div/form/div[1]/label/input"), "Ирина")

        #  вводим в поле с фамилией фамилию
        wait_and_send_keys(driver, (By.XPATH,
                                             "/html/body/div[2]/div/div/div[5]/div/div[2]/div/div[2]/div/div[1]/div/form/div[2]/label/input"), "Артамонова")

        # Заполняем поле с почтой
        wait_and_send_keys(driver, (By.XPATH,
                                             "/html/body/div[2]/div/div/div[5]/div/div[2]/div/div[2]/div/div[1]/div/form/span/div/label/input"), "irinaartamonova5@gmail.com")

        # Отжимаем чекбокс (галку) через JavaScript, потому что по-другому не отжимается
        checkbox1 = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.NAME, "isSubscribed"))
        )
        driver.execute_script("arguments[0].click();", checkbox1)

        # Нажимаем чекбокс (галку) с подтверждением 18 лет через JavaScript, потому что по-другому не нажимается
        checkbox2 = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.NAME, "isPolicyAgreed"))
        )
        driver.execute_script("arguments[0].click();", checkbox2)

        # жмем зарегистрироваться
        wait_and_click(driver, (By.XPATH,
                                         "/html/body/div[2]/div/div/div[5]/div/div[2]/div/div[2]/div/div[1]/div/form/button"))
        get_and_save_headers(driver, 'тестовые данные.ini', PROFILE_URL)
        logging.info("UI тест регистрация успешно завершен")