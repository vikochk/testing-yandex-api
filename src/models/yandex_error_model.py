from pydantic import BaseModel


class YandexErrorModel(BaseModel):
    error: str | None = None
    description: str | None = None
    message: str