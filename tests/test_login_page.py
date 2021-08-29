import allure
import time

from page_objects.LoginPage import LoginPage


@allure.parent_suite("Проверка тестового магазина opencart")
@allure.suite("Тесты страницы авторизации")
@allure.epic("Проверка магазина на opencart")
@allure.feature("Проверка наличия элементов на странице логина")
@allure.title("Поиск элементов на странице логина")
@allure.description("""Тест проверяет наличие элементов на странице логина""")
@allure.severity(allure.severity_level.CRITICAL)
def test_find_elements_login_page(browser):
    login_page = LoginPage(browser).open()
    login_page.find_input_email()
    login_page.find_continue_button()
    login_page.find_input_password()
    login_page.find_forgotten_password()
    login_page.find_login_button()


@allure.parent_suite("Проверка тестового магазина opencart")
@allure.suite("Тесты страницы авторизации")
@allure.epic("Проверка магазина на opencart")
@allure.feature("Проверка возможности входа и выхода как пользователь")
@allure.title("Вход на странице авторизации")
@allure.description("""Тест проверяет возможность входа и выхода, как пользователь на странице авторизации""")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_as_customer(browser):
    # pytest.skip('Причина пропуска теста')
    login_page = LoginPage(browser).open()
    login_page.click_add_user()
    login_page.fill_register_form('Ivan', 'Ivanov', 'test@ya.ru', '+79000551135', 'test')
    login_page.click_agree_and_continue()
    login_page.logout_as_customer()
    login_page.click_login_user_top()
    # allure.attach.file(source='attachments/no_match_for_email.png', attachment_type=allure.attachment_type.PNG)
    login_page.login_as_customer('test@ya.ru', 'test')
    login_page.logout_as_customer()
    login_page.verify_title('Account Logout')
    login_page.open_admin()
    login_page.login('user', 'bitnami')
    login_page.goto_all_customers()
    login_page.delete_customer()
