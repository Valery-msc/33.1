from __future__ import annotations

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
from selenium.webdriver.support.ui import WebDriverWait
from tests_data import Valid_Data
from tests_data import Invalid_Data
from tests.locators import RTPanelNaviBar
from tests.locators import RTAutorizationLocators
from tests.locators import RTAutorizationAllerts
from tests.locators import RTRegistrationLocators
import allure

fake_name = Faker().name()
fake_email = Faker().email()
fake_password = Faker().password()

@allure.story('TP-9501-Тесты_авторизации')
class TestValidRegistrationRT:

    def setup_method(self):
        self.open()

    def open(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://b2c.passport.rt.ru")
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.ID, RTRegistrationLocators.LOCATOR_RT_REGISTRATION_BUTTON_REGISTER)))

    def close(self):
        self.driver.quit()

    def teardown_method(self):
        self.close()

    def _get_element(self, locator_by: str, locator_value: str) -> WebElement | None:
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((locator_by, locator_value)))
        except TimeoutException as e:
            print(e)
        return None

    def _is_element_present(self, locator_by: str, locator_value: str) -> bool:
        return bool(self._get_element(locator_by, locator_value))

    def _is_element_text(self, locator_by: str, locator_value: str, text: str) -> bool:
        elem = self._get_element(locator_by, locator_value)
        if elem:
            return elem.text == text
        return False

    def _fill_field(self, locator_by: str, locator_value: str, value: str = ''):
        if value:
            elem = self._get_element(locator_by, locator_value)
            if elem:
                elem.send_keys(value)

    def _fill_form(self,
                   email: str = '',
                   password: str = ''):
        self._fill_field(By.ID, RTAutorizationLocators.LOCATOR_RT_AUTORIZATION_USER,
                         value=email)
        self._fill_field(By.ID,RTAutorizationLocators.LOCATOR_RT_AUTORIZATION_PASSWORD,
                         value=password)

    def _login(self):
        elem = self._get_element(
            By.ID,
            RTAutorizationLocators.LOCATOR_RT_AUTORIZATION_BUTTON_LOGIN)
        if elem:
            elem.click()

# 11
    @allure.feature('Проверка кликабельности бара выбора типа авторизации')
    def test_clicable_navi_bar(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, RTPanelNaviBar.LOCATOR_NAVI_BAR_LS))).click()
        assert self.driver.find_element(By.XPATH, RTPanelNaviBar.LOCATOR_FORM_LS)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, RTPanelNaviBar.LOCATOR_NAVI_BAR_MAIL))).click()
        assert self.driver.find_element(By.XPATH, RTPanelNaviBar.LOCATOR_FORM_MAIL)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, RTPanelNaviBar.LOCATOR_NAVI_BAR_LOGIN))).click()
        assert self.driver.find_element(By.XPATH, RTPanelNaviBar.LOCATOR_FORM_LOGIN)
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, RTPanelNaviBar.LOCATOR_NAVI_BAR_TELEPHONE))).click()
        assert self.driver.find_element(By.XPATH, RTPanelNaviBar.LOCATOR_FORM_TELEPHONE)

# 12
    @allure.feature('Авторизация с некорректным Email')
    def test_autorization_invalid_email(self):
        allure.step('Заполнение и отправка формы')
        self._fill_form(email=Invalid_Data.fake_email,
                        password=Invalid_Data.fake_password)
        self._login()
        with allure.step('Проверка наличия элемента'):
            assert self._is_element_present(
                By.XPATH,
                RTAutorizationAllerts.LOCATOR_RT_AUTORIZATION_ALLERTS_ERROR)
        with allure.step('Проверка текста элемента'):
            assert self._is_element_text(
                    By.XPATH, RTAutorizationAllerts.LOCATOR_RT_AUTORIZATION_ALLERTS_ERROR,
              'Неверно введен текст с картинки'
                    )

# 13
    @allure.feature('Авторизация с некорректным номером телефона')
    def test_autorization_invalid_phoneNumber(self):
        allure.step('Заполнение и отправка формы')
        self._fill_form(email=Invalid_Data.invalid_phoneNumber,
                        password=Valid_Data.valid_password)
        self._login()
        with allure.step('Проверка наличия элемента'):
            assert self._is_element_present(
                By.XPATH,
                RTAutorizationAllerts.LOCATOR_RT_AUTORIZATION_ALLERTS_ERROR)
        with allure.step('Проверка текста элемента'):
            assert self._is_element_text(
                By.XPATH, RTAutorizationAllerts.LOCATOR_RT_AUTORIZATION_ALLERTS_ERROR,
                'Неверно введен текст с картинки'
                )

# 14
    @allure.feature('Авторизация с некорректным паролем')
    def test_autorization_invalid_password(self):
        allure.step('Заполнение и отправка формы')
        self._fill_form(email=Valid_Data.valid_phoneNumber,
                        password=Invalid_Data.fake_password)
        self._login()
        with allure.step('Проверка наличия элемента'):
            assert self._is_element_present(
                By.XPATH,
                RTAutorizationAllerts.LOCATOR_RT_AUTORIZATION_ALLERTS_ERROR)
        with allure.step('Проверка текста элемента'):
            assert self._is_element_text(
                By.XPATH, RTAutorizationAllerts.LOCATOR_RT_AUTORIZATION_ALLERTS_ERROR,
                'Неверно введен текст с картинки')

# 15
    @allure.feature('Авторизация с XSS инъекцией')
    def test_autorization_xss_in_login(self):
        allure.step('Заполнение и отправка формы')
        self._fill_form(email=Invalid_Data.xss,
                        password=Invalid_Data.fake_password)
        self._login()
        with allure.step('Проверка наличия элемента'):
            assert self._is_element_present(
                By.XPATH,
                RTAutorizationAllerts.LOCATOR_ERROR_TEXT_XSS)
