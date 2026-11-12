from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.locator.locator import Locator


class AuthorizationWithFingerprintForm(Form):
    def __init__(self):
        super().__init__(
            Locator.by_xpath('//*[@data-testid="page-webauthn-reg-start"]'), 
            'Форма активации авторизации по лицу или отпечатку пальца'
        )
        
        self.next_button = self._element_factory.get_button(
            Locator.by_xpath('//button[@data-testid="webauthn-reg-later-button"]'), 
            'Кнопка отказа от активации для перехода в следующую форму'
        )

    def go_to_the_next_page(self):
        self.next_button.click_and_wait()