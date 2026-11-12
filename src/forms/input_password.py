from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.locator.locator import Locator


class AuthorizationPasswordForm(Form):
    def __init__(self):
        super().__init__(
            Locator.by_xpath('//*[@data-testid="password-input"]'), 
            'Форма авторизации по паролю'
        )
        
        self.password_textbox = self._element_factory.get_text_box(
            Locator.by_xpath('//input[@data-testid="text-field-input"]'), 
            'Поле ввода для авторизации по паролю'
        )

        self.next_button = self._element_factory.get_button(
            Locator.by_xpath('//button[@data-testid="password-next"]'), 
            'Кнопка перехода в следующую форму'
        )

    def input_password(self, password):
        self.password_textbox.clear_and_type(password)

    def go_to_the_next_page(self):
        self.next_button.click_and_wait()