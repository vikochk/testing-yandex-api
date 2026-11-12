from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.locator.locator import Locator


class YandexDiskUnauthorizedForm(Form):
    def __init__(self):
        super().__init__(
            Locator.by_xpath('//button[@id="header-button-connect"]'), 
            'Страница Яндекс диск неавторизованного пользователя'
        )

        self.authorize_button = self._element_factory.get_button(
            Locator.by_xpath('//a[@id="header-login-button"]'), 
            'Кнопка для входа в аккаунт'
        )

    def start_authorization(self):
        self.authorize_button.click()