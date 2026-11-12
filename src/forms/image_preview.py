import io
from PIL import ImageStat, ImageChops, Image
from py_selenium_auto.forms.form import Form
from py_selenium_auto_core.logging.logger import Logger
from py_selenium_auto_core.locator.locator import Locator


class ImageFileForm(Form):
    def __init__(self):
        current_image_locator = Locator.by_xpath('//img[contains(@class, "scalable-preview__image")]')
        super().__init__(current_image_locator, 'Форма открытого файла с изображением')

        self.image_element = self._element_factory.get_label(
            current_image_locator, 'Элемент изображения'
        )

        self.close_button = self._element_factory.get_button(
            Locator.by_xpath('//button[@aria-label="Закрыть" and @data-testid="orb-button"]'),
            'Кнопка для закрытия файла с изображением'
        )

    def is_chosen_image_displayed(self, expected_image_bytes: bytes, tolerance: float = 0.80) -> bool:
        Logger.info('Ожидание отображения элемента изображения на экране браузера')
        self.image_element.state.wait_for_displayed()

        Logger.info('Снятие скриншота элемента изображения с экрана')
        actual_screenshot_bytes = self.image_element.get_element().screenshot_as_png

        Logger.info('Инициализация объектов изображений через Pillow и перевод в RGB')
        actual_img = Image.open(io.BytesIO(actual_screenshot_bytes)).convert('RGB')
        expected_img = Image.open(io.BytesIO(expected_image_bytes)).convert('RGB')

        Logger.info('Масштабирование эталонного изображения под размер скриншота')
        expected_img_resized = expected_img.resize(actual_img.size)

        Logger.info('Вычисление разницы между изображениями')
        diff = ImageChops.difference(expected_img_resized, actual_img)
        
        stat = ImageStat.Stat(diff)
        rms_difference = sum(stat.rms) / len(stat.rms)
        
        similarity = 1.0 - (rms_difference / 255.0)
        
        Logger.info(f'Рассчитанное сходство изображений: {similarity:.2%} (порог: {tolerance:.2%})')
        return similarity >= tolerance
    
    def close_photo(self):
        self.close_button.click()