from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.locator.locator import Locator


class AuthorizationForm(Form):
    def __init__(self):
        super().__init__(
            Locator.by_xpath('//*[@data-testid="segment-picker"]'), 
            'Форма авторизации по логину, email или номеру телефона'
        )
        
        self.login_and_email_textbox = self._element_factory.get_text_box(
            Locator.by_xpath('//input[@type="text"]'), 
            'Поле ввода для авторизации по логину или email'
        )

        self.next_page_button = self._element_factory.get_button(
            Locator.by_xpath('//button[@data-testid="add-user-next"]'), 
            'Кнопка перехода в следующую форму'
        )

    def input_login_or_email(self, login):
        self.login_and_email_textbox.clear_and_type(login)

    def go_to_the_next_page(self):
        self.next_page_button.click_and_wait()