from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.logging.logger import Logger
from py_selenium_auto_core.locator.locator import Locator
from selenium.common.exceptions import NoSuchElementException


class AuthorizationPushNotificationForm(Form):
    def __init__(self):
        super().__init__(
            Locator.by_xpath('//*[contains(@data-testid, "code-input")]'), 
            'Форма авторизации по пуш-уведомлению'
        )
        
        self.login_with_password_button = self._element_factory.get_button(
            Locator.by_xpath('//button[@data-testid="password-btn"]'), 
            'Кнопка перехода в форму авторизации по паролю'
        )

    def go_to_password_form(self):
        try:
            self.login_with_password_button.get_element()
            self.login_with_password_button.click_and_wait()
        except NoSuchElementException as e:
            Logger.fatal('Кнопка для ввода пароля недоступна')
            raise e