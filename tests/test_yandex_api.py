import hashlib
from http import HTTPStatus
from py_selenium_auto_core.logging.logger import Logger
from py_selenium_auto.browsers.browser_services import BrowserServices

from src.utils.browser_manager import BrowserManager
from src.utils.random_generation import RandomGeneration
from src.api.yandex_api_client import RootLocation

from src.forms.text_file import TextFileForm
from src.forms.image_preview import ImageFileForm
from src.forms.yandex_files import YandexFilesForm
from src.forms.authorization import AuthorizationForm
from src.forms.input_password import AuthorizationPasswordForm
from src.forms.input_push import AuthorizationPushNotificationForm
from src.forms.yandex_disk_unauthorized import YandexDiskUnauthorizedForm
from src.forms.authorization_with_fingerprint import AuthorizationWithFingerprintForm


class TestYandexApi:
    def test_yandex_api(self, api_client, test_user, test_params, image):
        Logger.info('[Шаг 1: UI] Перейти на сайт '
                    f'{BrowserServices.Instance.service_provider.settings_file().get("base_url")}')
        unauthorized_form = YandexDiskUnauthorizedForm()

        Logger.info('Проверка отображения страницы неавторизованного пользователя')
        assert unauthorized_form.state.is_displayed(), \
            'Страница неавторизованного пользователя на диске не была открыта'

        Logger.info('[Шаг 2: UI] Авторизоваться')
        auth_form = AuthorizationForm()
        auth_with_push_form = AuthorizationPushNotificationForm()
        auth_with_password_form = AuthorizationPasswordForm()
        auth_with_fingerprint_form = AuthorizationWithFingerprintForm()
        files_form = YandexFilesForm()

        Logger.info('Клик по кнопке начала авторизации')
        unauthorized_form.start_authorization()

        assert auth_form.state.wait_for_displayed(
            BrowserServices.Instance.service_provider.timeout_configuration().page_load
        ), 'Форма для авторизации по логину, email или телефону не была открыта'

        Logger.info(f'Ввод логина/email: {test_user.login}')
        auth_form.input_login_or_email(test_user.login)
        auth_form.go_to_the_next_page()

        if auth_with_push_form.state.is_displayed():
            Logger.info('Обнаружен шаг подтверждения по пуш-уведомлению. Переключение на форму пароля')
            auth_with_push_form.go_to_password_form()

        assert auth_with_password_form.state.wait_for_displayed(
            BrowserServices.Instance.service_provider.timeout_configuration().page_load
        ), 'Форма для авторизации по паролю не была открыта'

        Logger.info('Ввод пароля тестового пользователя')
        auth_with_password_form.input_password(test_user.password)
        auth_with_password_form.go_to_the_next_page()

        if auth_with_push_form.state.is_displayed():
            Logger.info('Обнаружен шаг подтверждения по пуш-уведомлению. Переключение на ожидание действий пользователя')
            assert auth_with_push_form.state.wait_for_not_displayed(
                BrowserServices.Instance.service_provider.timeout_configuration().command
            ), 'Пользователь не ввел код из пуш-уведомления в течение 2 минут'

        if auth_with_fingerprint_form.state.is_displayed():
            Logger.info('Пропуск окна авторизации по отпечатку пальца')
            auth_with_fingerprint_form.go_to_the_next_page()

        Logger.info('Проверка успешного входа на Яндекс Диск')
        assert files_form.state.wait_for_displayed(
            BrowserServices.Instance.service_provider.timeout_configuration().page_load
        ), 'Окно с файлами на диске пользователя не было открыто'

        Logger.info('[Шаг 3: API] С помощью запроса к API добавить текстовый файл со случайным текстом, '
                    f'убедиться что ответ вернулся с кодом {test_params.initial_file.expected_upload_status}')
        Logger.info('Генерация случайной текстовой строки')
        random_text = RandomGeneration.generate_string()

        Logger.info(f'Загрузка файла {test_params.initial_file.name} на Яндекс Диск через API')
        upload_link_response = api_client.upload_file(
            file_content=random_text,
            destination=test_params.initial_file.name,
            overwrite=True
        )
        Logger.info(f'Проверка статуса ответа API. Получен код: {upload_link_response.status_code}')
        assert upload_link_response.status_code == test_params.initial_file.expected_upload_status, \
            f'Файл {test_params.initial_file.name} не был создан через API'

        Logger.info('[Шаг 4: UI] Не обновляя страницу убедиться, что добавленный файл появился на диске, '
                    'имя файла соответствует отправленному')
        Logger.info(f'Ожидание появления файла {test_params.initial_file.name} в браузере')
        assert files_form.wait_for_file_to_appeare(test_params.initial_file.name), \
            f'Файл с названием {test_params.initial_file.name} не был загружен на диск'
        
        Logger.info('[Шаг 5: UI] Открыть документ в новой вкладке, убедиться что содержимое документа '
                    'соответствует содержимому в отправленном файле, закрыть вкладку')
        text_file_form = TextFileForm()
        
        Logger.info(f'Двойной клик на файл {test_params.initial_file.name}')
        files_form.double_click_on_file(test_params.initial_file.name)
        
        Logger.info('Переключение драйвера на открывшуюся вкладку с документом')
        BrowserManager.open_last_tab()
        
        assert text_file_form.state.wait_for_displayed(
            BrowserServices.Instance.service_provider.timeout_configuration().script
        ), f'Страница с файлом {test_params.initial_file.name} не была открыта'
        
        Logger.info('Чтение текстового контента из открытой вкладки и сравнение с отправленным')
        assert text_file_form.get_text_from_file() == random_text, \
            'Содержимое открытого текстового документа не соответствует отправленному'
        
        Logger.info('Закрытие вкладки документа и возврат к списку файлов Диска')
        BrowserManager.close_current_and_switch_to_first_tab()

        Logger.info('[Шаг 6: API] Изменить расширение файла на диске на jpg, используя API запрос, '
                    f'убедиться, что получен ответ с кодом {test_params.renamed_file.expected_rename_status}')
        new_file_name = test_params.initial_file.name.split('.')[0] + test_params.renamed_file.name_ending
        
        Logger.info(f'Отправка API-запроса на переименование файла "{test_params.initial_file.name}" в "{new_file_name}"')
        move_response = api_client.move_or_rename_resource(
            from_name=test_params.initial_file.name,
            to_name=new_file_name
        )
        Logger.info(f'Проверка статуса ответа API. Получен код: {move_response.status_code}')
        assert move_response.status_code == test_params.renamed_file.expected_rename_status, \
            'Не удалось изменить расширение файла через API'

        Logger.info('[Шаг 7: UI] Не обновляя страницу убедиться, что расширение файла изменилось')
        Logger.info(f'Ожидание появления {new_file_name} и исчезновения {test_params.initial_file.name}')
        assert files_form.wait_for_file_to_appeare(new_file_name) and files_form.wait_for_file_to_disappeare(test_params.initial_file.name), \
            f'Файл с названием {new_file_name} не появился на диске или файл {test_params.initial_file.name} не исчез'

        Logger.info('[Шаг 8: API] Загрузить изображение с тем же именем файла, что и измененный '
                    f'в предыдущем шаге с заменой, получен код ответа {test_params.renamed_file.expected_overwrite_status}')
        
        Logger.info('Читаем файл с диска в бинарном режиме')
        try:
            with open(image, "rb") as image_file:
                real_image_bytes = image_file.read()
            Logger.info(f'Файл успешно прочитан. Размер: {len(real_image_bytes)} байт')

            file_md5 = hashlib.md5(real_image_bytes).hexdigest()
        except Exception as e:
            Logger.fatal(f"Ошибка при открытии файла: {e}")

        Logger.info(f'Перезапись файла {new_file_name} графическими данными')
        upload_image_response = api_client.upload_file(
            file_content=real_image_bytes,
            destination=new_file_name,
            overwrite=True
        )
        Logger.info(f'Проверка статуса ответа API. Получен код: {upload_image_response.status_code}')
        assert upload_image_response.status_code == test_params.renamed_file.expected_overwrite_status, \
            'Не удалось перезаписать изображение через API'

        Logger.info('[Шаг 9: UI] Открыть изображение, убедиться, что изображение соответствует '
                    'загруженному в предыдущем шаге. Закрыть изображение')
        BrowserManager.refresh_page()

        Logger.info(f'Двойной клик для открытия изображения {new_file_name}')
        files_form.double_click_on_file(new_file_name)
        
        image_preview_form = ImageFileForm()
        assert image_preview_form.state.wait_for_displayed(), 'Окно просмотра изображения не было открыто'
        
        Logger.info('Запуск попиксельного визуального сравнения изображения на UI с загруженным оригиналом')
        assert image_preview_form.is_chosen_image_displayed(real_image_bytes), \
            'Изображение на диске (на UI) не соответствует загруженному файлу'
        
        Logger.info('Закрытие окна просмотра изображения')
        image_preview_form.close_photo()

        Logger.info('[Шаг 10: UI] Перетащить файл с изображением в корзину')
        Logger.info(f'Перетаскивание файла {new_file_name} в корзину через UI')
        files_form.drag_file_to_trash(new_file_name)

        Logger.info('[Шаг 11: API] С помощью API запроса убедиться, что файл из предыдущего шага находится в корзине')
        Logger.info('Запрос списка файлов в корзине через API')
        trash_list_response = api_client.get_trash_list()
        assert trash_list_response.status_code == HTTPStatus.OK, 'Не удалось получить список файлов в корзине'

        Logger.info('Поиск удаленного файла в списке ресурсов корзины по имени')
        trash_items = []
        if trash_list_response.data and trash_list_response.data.embedded:
            trash_items = trash_list_response.data.embedded.items

        Logger.info(f'Поиск удаленного файла по MD5 хэшу: {file_md5}')
        target_file = next((item for item in trash_items if item.md5 == file_md5), None)
        assert target_file is not None, f'Файл с хэшем {file_md5} не найден в корзине'

        real_trash_path = target_file.path
        Logger.info(f'Файл найден в корзине. Уникальный путь: {real_trash_path}')

        Logger.info('Запрос данных конкретного файла из корзины по полученному пути')
        trash_file_response = api_client.get_trash_resource(real_trash_path)
        Logger.info(f'Проверка ответа API. Получен код: {trash_file_response.status_code}')
        assert trash_file_response.status_code == HTTPStatus.OK, \
            'Запрос информации о файле в корзине вернул неверный статус'
        assert trash_file_response.data.name == new_file_name, \
            'Имя файла в корзине не соответствует ожидаемому'
        assert trash_file_response.data.type == test_params.renamed_file.expected_type_in_trash, \
            'Тип объекта в корзине определен неверно'

        Logger.info('[Шаг 12: API] Через запрос к API восстановить файл из предыдущего шага из корзины')
        Logger.info(f'Отправка запроса на восстановление ресурса {real_trash_path}')
        restore_response = api_client.restore_trash_resource(real_trash_path)
        Logger.info(f'Проверка ответа API. Получен код: {restore_response.status_code}')
        assert restore_response.status_code == test_params.renamed_file.expected_restore_status, \
            'Не удалось восстановить файл из корзины через API'

        Logger.info('[Шаг 13: UI] Не обновляя страницу убедиться, что изображение вновь присутствует на диске')
        Logger.info(f'Ожидание появления восстановленного файла {new_file_name} на диске')
        assert files_form.wait_for_file_to_appeare(new_file_name), \
            f'Восстановленный файл {new_file_name} не появился на диске'

        Logger.info('[Шаг 14: API] Используя запрос к API безвозвратно удалить изображение из Диска, ' 
                    f'убедиться, что получен ответ с кодом {test_params.renamed_file.expected_delete_status}')
        Logger.info(f'Отправка запроса на окончательное удаление файла {new_file_name}')
        delete_response = api_client.delete_resource(new_file_name, location=RootLocation.DISK, permanently=True)
        Logger.info(f'Проверка ответа API. Получен код: {delete_response.status_code}')
        assert delete_response.status_code == test_params.renamed_file.expected_delete_status, \
            'Не удалось безвозвратно удалить файл через API'

        Logger.info('[Шаг 15: UI] Не обновляя страницу убедиться, что изображение отсутствует на диске.')
        BrowserManager.refresh_page()
        Logger.info(f'Ожидание исчезновения файла {new_file_name} из списка файлов Диска')
        assert files_form.wait_for_file_to_disappeare(new_file_name), \
            f'Удаленный файл {new_file_name} все еще присутствует в списке файлов'