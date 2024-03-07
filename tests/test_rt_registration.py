from __future__ import annotations

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from faker import Faker
from tests_data import Valid_Data
from tests_data import Invalid_Data
from tests.locators import RTRegistrationLocators
from tests.locators import RTRegistrationsAllerts
import allure

fake_name = Faker().name()
fake_email = Faker().email()
fake_password = Faker().password()

@allure.story('TP-9501-Тесты_регистрации')

class TestValidRegistrationRT:


    def setup_method(self):
        self.open()


    def open(self):
        self.driver = webdriver.Chrome(service=ChromeService(executable_path=ChromeDriverManager().install()))
        self.driver.get("https://b2c.passport.rt.ru")
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, RTRegistrationLocators.LOCATOR_RT_REGISTRATION_BUTTON_REGISTER)))
        button.click()

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
                    first_name: str = '',
                    last_name: str = '',
                    email: str = '',
                    password: str = '',
                    confirm_password: str = ''):
        confirm_password = confirm_password or password
        self._fill_field(By.XPATH, RTRegistrationLocators.LOCATOR_RT_REGISTRATION_FIRSTNAME,
                             value=first_name)
        self._fill_field(By.XPATH, RTRegistrationLocators.LOCATOR_RT_REGISTRATION_LASTNAME,
                             value=last_name)
        self._fill_field(By.ID, RTRegistrationLocators.LOCATOR_RT_REGISTRATION_NUMBER_OR_EMAIL,
                             value=email)
        self._fill_field(By.ID, RTRegistrationLocators.LOCATOR_RT_REGISTRATION_PASSWORD,
                             value=password)
        self._fill_field(By.ID, RTRegistrationLocators.LOCATOR_RT_REGISTRATION_PASSWORD_CONFIRM,
                             value=confirm_password)

    def _submit_form(self):
        elem = self._get_element(
            locator_by=By.XPATH,
            locator_value=RTRegistrationLocators.LOCATOR_RT_REGISTRATION_BUTTON_SUBMIT)
        if elem:
            elem.click()

    def test_eto_baza(self):
        self._fill_form(first_name=Valid_Data.valid_first_name,
                        last_name=Valid_Data.valid_last_name,
                        email=Invalid_Data.fake_email,
                        password=Invalid_Data.fake_password)
        self._submit_form()
        assert self._is_element_present(By.ID,
        RTRegistrationLocators.LOCATOR_RT_REGISTRATION_ENTER_CODE)

# 1
    @allure.feature('Регистрация с паролем из 21 символа')
    def test_registration_user_with_pass_21char(self):
        allure.step('Заполнение и отправка формы')
        self._fill_form(first_name=Valid_Data.valid_first_name,
                    last_name=Valid_Data.valid_last_name,
                    email=Invalid_Data.fake_email,
                    password=Invalid_Data.password_21_char)
        self._submit_form()
        with allure.step('Проверка наличия элемента'):
            assert self._is_element_present(
            By.XPATH,
            RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR)
        with allure.step('Проверка текста элемента'):
            assert self._is_element_text(
        By.XPATH,
        RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR,
        'Длина пароля должна быть не более 20 символов')

# 2
    @allure.feature('Регистрация с Email без домена')
    def test_registration_user_with_email_without_domain(self):
        allure.step('Заполнение и отправка формы')
        self._fill_form(first_name=Valid_Data.valid_first_name,
                    last_name=Valid_Data.valid_last_name,
                    email=Invalid_Data.email_without_domain,
                    password=Invalid_Data.fake_password)
        self._submit_form()
        with allure.step('Проверка наличия элемента'):
            assert self._is_element_present(
        By.XPATH,
        RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR)
        with allure.step('Проверка текста элемента'):
            assert self._is_element_text(
        By.XPATH,
        RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR,
        'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, '
        'или email в формате example@email.ru')

# 3
    @allure.feature('Регистрация с именем из 31 символа')
    def test_registration_user_with_firstname_31char(self):
        allure.step('Заполнение и отправка формы')
        self._fill_form(first_name=Invalid_Data.first_name_31_char,
                    last_name=Valid_Data.valid_last_name,
                    email=Invalid_Data.fake_email,
                    password=Invalid_Data.fake_password)
        self._submit_form()
        with allure.step('Проверка наличия элемента'):
            assert self._is_element_present(
            By.XPATH,
            RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR)
        with allure.step('Проверка текста элемента'):
            assert self._is_element_text(
            By.XPATH, RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR,
            'Необходимо заполнить поле кириллицей. От 2 до 30 символов.')

# 4
    @allure.feature('Регистрация с именем из 1 символа')
    def test_registration_user_with_firstname_1char(self):
        allure.step('Заполнение и отправка формы')
        self._fill_form(first_name=Invalid_Data.first_name_1_char,
                        last_name=Valid_Data.valid_last_name,
                        email=Invalid_Data.fake_email,
                        password=Invalid_Data.fake_password)
        self._submit_form()
        with allure.step('Проверка наличия элемента'):
            assert self._is_element_present(
                By.XPATH,
                RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR)
        with allure.step('Проверка текста элемента'):
            assert self._is_element_text(
                By.XPATH, RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR,
                'Необходимо заполнить поле кириллицей. От 2 до 30 символов.')

# 5
    @allure.feature('Регистрация с незаполненным обязательным полем Email или Телефон')
    def test_registration_user_with_not_filled_email_or_mobile(self):
        allure.step('Заполнение и отправка формы')
        self._fill_form(first_name=Valid_Data.valid_first_name,
                        last_name=Valid_Data.valid_last_name,
                        password=Invalid_Data.fake_password)
        self._submit_form()
        with allure.step('Проверка наличия элемента'):
            assert self._is_element_present(
                By.XPATH,
                RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR)
        with allure.step('Проверка текста элемента'):
            assert self._is_element_text(
                By.XPATH, RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR,
                'Введите телефон в формате +7ХХХХХХХХХХ или +375XXXXXXXXX, '
                'или email в формате example@email.ru')

# 6
    @allure.feature('Регистрация с незаполненным обязательным полем Фамилия')
    def test_registration_user_with_not_filled_lastname(self):
        allure.step('Заполнение и отправка формы')
        self._fill_form(first_name=Valid_Data.valid_first_name,
                        email=Invalid_Data.fake_email,
                        password=Invalid_Data.fake_password)
        self._submit_form()
        with allure.step('Проверка наличия элемента'):
            assert self._is_element_present(
                By.XPATH,
                RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR)
        with allure.step('Проверка текста элемента'):
            assert self._is_element_text(
                By.XPATH, RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR,
                'Необходимо заполнить поле кириллицей. От 2 до 30 символов.')

# 7
    @allure.feature('Регистрация с незаполненным обязательным полем Имя')
    def test_registration_user_with_not_filled_firstname(self):
        allure.step('Заполнение и отправка формы')
        self._fill_form(last_name=Valid_Data.valid_last_name,
                        email=Invalid_Data.fake_email,
                        password=Invalid_Data.fake_password)
        self._submit_form()
        with allure.step('Проверка наличия элемента'):
            assert self._is_element_present(
                By.XPATH,
                RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR)
        with allure.step('Проверка текста элемента'):
            assert self._is_element_text(
                By.XPATH, RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR,
                'Необходимо заполнить поле кириллицей. От 2 до 30 символов.')

# 8
    @allure.feature('Регистрация с несовпадающими паролями')
    def test_registration_user_with_non_matching_passwords(self):
        allure.step('Заполнение и отправка формы')
        self._fill_form(first_name=Valid_Data.valid_first_name,
                        last_name=Valid_Data.valid_last_name,
                        email=Invalid_Data.fake_email,
                        password=Invalid_Data.fake_password,
                        confirm_password=Invalid_Data.fake_password_reg)
        self._submit_form()
        with allure.step('Проверка наличия элемента'):
            assert self._is_element_present(
                By.XPATH,
                RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR)
        with allure.step('Проверка текста элемента'):
            assert self._is_element_text(
                By.XPATH, RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR,
                'Пароли не совпадают')

# 9
    @allure.feature('Регистрация с паролем не содержащем цифру')
    def test_registration_user_with_password_not_contain_digit(self):
        allure.step('Заполнение и отправка формы')
        self._fill_form(first_name=Valid_Data.valid_first_name,
                        last_name=Valid_Data.valid_last_name,
                        email=Invalid_Data.fake_email,
                        password=Invalid_Data.password_not_contain_digit)
        self._submit_form()
        with allure.step('Проверка наличия элемента'):
            assert self._is_element_present(
                By.XPATH,
                RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR)
        with allure.step('Проверка текста элемента'):
            assert self._is_element_text(
                By.XPATH, RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR,
                'Пароль должен содержать хотя бы 1 спецсимвол или хотя бы одну цифру')

# 10
    @allure.feature('Регистрация с фамилией из 31 символа')
    def test_registration_user_with_lastname_31char(self):
        allure.step('Заполнение и отправка формы')
        self._fill_form(first_name=Valid_Data.valid_first_name,
                        last_name=Invalid_Data.last_name_31_char,
                        email=Invalid_Data.fake_email,
                        password=Invalid_Data.fake_password)
        self._submit_form()
        with allure.step('Проверка наличия элемента'):
            assert self._is_element_present(
                By.XPATH,
                RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR)
        with allure.step('Проверка текста элемента'):
            assert self._is_element_text(
                    By.XPATH, RTRegistrationsAllerts.LOCATOR_RT_REGISTRATION_ALLERTS_ERROR,
                    'Необходимо заполнить поле кириллицей. От 2 до 30 символов.')
