from enum import StrEnum


class RootLocation(StrEnum):
    DISK = 'disk:/'
    TRASH = 'trash:/'


class ContentType(StrEnum):
    JSON = 'application/json'