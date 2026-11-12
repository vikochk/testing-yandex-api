from pathlib import Path
from typing import TypeVar, Any
from pydantic import ValidationError, TypeAdapter
from py_selenium_auto_core.logging.logger import Logger
from py_selenium_auto_core.utilities.file_reader import FileReader
from py_selenium_auto_core.utilities.root_path_helper import RootPathHelper


T = TypeVar('T')


class TestDataProvider:
    __test__ = False

    TEST_USER_DATA_FILENAME = 'test_user_data.json'
    YANDEX_DISK_DATA_FILENAME = 'yandex_disk_data.json'

    @staticmethod
    def get_test_data(file_name: str, data_type: Any) -> T:
        tests_root = Path(RootPathHelper.calling_root_path())

        if not FileReader.is_resource_file_exist(file_name, tests_root):
            Logger.fatal(
                f"Файл с тестовыми данными '{file_name}' не был найден по пути '{tests_root}'", 
                FileNotFoundError
            )

        try:
            raw_json = FileReader.get_resource_file(file_name, tests_root)
            adapter = TypeAdapter(data_type)
            return adapter.validate_json(raw_json)
        
        except (ValidationError, ValueError) as e:
            Logger.fatal(
                f'Неверная структура файла с тестовыми данными: {e}', ValueError
            )
            raise e 