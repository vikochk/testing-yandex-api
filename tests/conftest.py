import os
from pathlib import Path

work_dir = str(Path(__file__).resolve().parent)
os.chdir(work_dir)

import pytest
from py_selenium_auto_core.logging.logger import Logger
from py_selenium_auto.browsers.browser_services import BrowserServices

from src.utils.test_manager import TestDataProvider
from src.api.yandex_api_client import YandexApiClient
from src.models.test_data_model import TestDataModel
from src.models.yandex_disk_params_model import YandexDiskParamsModel


@pytest.fixture(scope="session")
def test_user():
    return TestDataProvider.get_test_data(
        TestDataProvider.TEST_USER_DATA_FILENAME, TestDataModel
    )


@pytest.fixture(scope="session")
def test_params():
    return TestDataProvider.get_test_data(
        TestDataProvider.YANDEX_DISK_DATA_FILENAME, YandexDiskParamsModel
    )

@pytest.fixture(scope="session")
def image():
    image_filepath = Path(__file__).resolve().parent / "resources" / "test.jpg"

    if not image_filepath.exists():
        raise FileNotFoundError(f"Тестовое изображение не найдено по пути: {image_filepath}")
    
    return image_filepath


@pytest.fixture(scope="session")
def api_client(test_user):
    return YandexApiClient(test_user.oauth)


@pytest.fixture(scope="session", autouse=True)
def setup_session():
    Logger.info(f"Установлена рабочая директория: {work_dir}")
    yield
    Logger.info("Завершение тестовой сессии")


@pytest.fixture(scope="function", autouse=True)
def setup_function():
    Logger.info("Запуск браузера")
    BrowserServices.Instance.browser.maximize()
    BrowserServices.Instance.browser.go_to(BrowserServices.Instance.service_provider\
                  .settings_file().get("base_url"))
    BrowserServices.Instance.browser.wait_for_page_to_load()
    yield
    if BrowserServices.Instance.is_browser_started:
        Logger.info("Закрытие браузера")
        BrowserServices.Instance.browser.quit()