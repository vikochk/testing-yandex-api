from http import HTTPStatus
from pydantic import TypeAdapter
from typing import Generic, TypeVar
from requests import Response as RequestsResponse

T = TypeVar('T')


class Response(Generic[T]):
    def __init__(self, raw_response: RequestsResponse, model_type: type[T] | None = None):
        self.raw = raw_response
        self.status_code = HTTPStatus(raw_response.status_code)
        self.text = raw_response.text
        self._model_type = model_type
        self._data = None

    @property
    def data(self) -> T:
        if self._data is None and self._model_type is not None:
            if self.text:
                adapter = TypeAdapter(self._model_type)
                self._data = adapter.validate_json(self.text)
        return self._data

    def json(self):
        return self.raw.json()