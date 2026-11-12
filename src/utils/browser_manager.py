from selenium.webdriver.support.ui import WebDriverWait
from py_selenium_auto.browsers.browser_services import BrowserServices


class BrowserManager:
    @staticmethod
    def open_last_tab(timeout: int = BrowserServices.Instance.service_provider.timeout_configuration().page_load):
        WebDriverWait(BrowserServices.Instance.browser.driver, timeout).until(
            lambda d: len(d.window_handles) > 1
        )
        BrowserServices.Instance.browser.tabs.switch_to_last_tab()

    @staticmethod
    def close_current_and_switch_to_first_tab():
        BrowserServices.Instance.browser.tabs.switch_to_first_tab(close_current=True)

    @staticmethod
    def refresh_page():
        BrowserServices.Instance.browser.refresh()