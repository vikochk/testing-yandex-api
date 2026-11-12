from selenium.webdriver import ActionChains
from py_selenium_auto.forms.form import Form
from py_selenium_auto.elements.button import Button
from py_selenium_auto_core.locator.locator import Locator
from py_selenium_auto.browsers.browser_services import BrowserServices


class YandexFilesForm(Form):
    def __init__(self):
        files_and_folders_locator = Locator.by_xpath('//*[@class="listing__items"]')

        super().__init__(files_and_folders_locator, 'Форма с файлами пользователя')

        self.files_and_folders_list = self._element_factory.get_text_box(
            files_and_folders_locator, 'Контейнер для всех файлов и папок в корне диска'
        )

        self.trash_button = self._element_factory.get_button(
            Locator.by_xpath('//*[@id="/trash"]'),
            'Кнопка мусорки'
        )

        self._all_files_locator = Locator.by_xpath(
            '//*[contains(@class, "item_type_file")]//*[contains(@class, "listing-item__title")]'
        )

        self._single_file_locator = '//*[contains(@class, "item_type_file")]' \
            '//*[contains(@class, "listing-item__title") and @aria-label="{}"]'

        self._single_file_icon_locator = '//div[contains(@class, "listing-item")][.//div[@aria-label="{}"]]'\
            '//div[contains(@class, "listing-item__icon")]'
        
    def get_all_files(self) -> list[Button]:
        files = self.files_and_folders_list.find_child_elements(
            Button, self._all_files_locator
        )
        return files
    
    def get_all_file_names(self) -> list[str]:
        files = self.get_all_files()
        return [file.get_attribute('aria-label') for file in files]

    def _get_file_locator(self, filename) -> Locator:
        return Locator.by_xpath(self._single_file_locator.format(filename))

    def _get_file_button(self, filename) -> Button:
        locator = self._get_file_locator(filename)
        return self._element_factory.get_button(locator, f'Кнопка файла: {filename}')

    def _get_file_icon_button(self, filename) -> Button:
        locator = Locator.by_xpath(self._single_file_icon_locator.format(filename))
        return self._element_factory.get_button(locator, f'Иконка файла: {filename}')

    def double_click_on_file(self, filename):
        file_button = self._get_file_button(filename)
        file_button.state.wait_for_clickable()
        
        web_element = file_button.get_element()
        
        actions = ActionChains(BrowserServices.Instance.browser.driver)
        actions.double_click(web_element).perform()

    def is_file_in_files(self, filename) -> bool:
        file_button = self._get_file_button(filename)
        return file_button.state.is_displayed()
    
    def drag_file_to_trash(self, filename):
        file_icon = self._get_file_icon_button(filename)
        
        file_web_element = file_icon.get_element()
        trash_web_element = self.trash_button.get_element()

        actions = ActionChains(BrowserServices.Instance.browser.driver)
        actions.click_and_hold(file_web_element) \
               .move_to_element(trash_web_element) \
               .move_by_offset(5, 5) \
               .pause(1) \
               .release() \
               .perform()
        
    def wait_for_file_to_disappeare(self, filename, 
                timeout: int = BrowserServices.Instance.service_provider.timeout_configuration().page_load) -> bool:
        file_button = self._get_file_button(filename)
        return file_button.state.wait_for_not_displayed(timeout)

    def wait_for_file_to_appeare(self, filename, 
                timeout: int = BrowserServices.Instance.service_provider.timeout_configuration().page_load) -> bool:
        file_button = self._get_file_button(filename)
        return file_button.state.wait_for_displayed(timeout)