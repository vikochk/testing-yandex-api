from selenium.webdriver.common.by import By
from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.locator.locator import Locator


class TextFileForm(Form):
    def __init__(self):
        super().__init__(
            Locator.by_xpath('//*[contains(@class, "page_text")]'), 
            'Форма открытого текстового файла'
        )

        self.host_element = self._element_factory.get_label(
            Locator.by_css_selector('.__page-1'), 
            'Элемент-родитель теневого DOM'
        )

        self.css_selector_of_text = '.mg1'
    
    def get_text_from_file(self):
        host = self.host_element.get_element()
        shadow_root = host.shadow_root

        text_web_element = shadow_root.find_element(By.CSS_SELECTOR, self.css_selector_of_text)

        text = text_web_element.text
        return text