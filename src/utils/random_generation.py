import random
import string
from typing import List
from py_selenium_auto_core.logging.logger import Logger


class RandomGeneration:
    @staticmethod
    def generate_string(
        length: int = 10, 
        required_groups: List[str] | None = None,
        mandatory_symbols: str = '',
        base_chars: str = string.ascii_lowercase
    ):
        if not isinstance(length, int) or length <= 0:
            Logger.warn('Длина строки имеет некорректный формат, берем значение по умолчанию')
            length = 10

        required_groups = required_groups or []
        result = []

        for group in required_groups:
            if group:
                result.append(random.choice(group))
                base_chars += group

        if mandatory_symbols:
            result.extend(list(mandatory_symbols))
            base_chars += mandatory_symbols

        if len(result) < length:
            while len(result) < length:
                result.append(random.choice(base_chars))
        elif len(result) > length:
            result = result[:length]

        random.shuffle(result)
        return ''.join(result)