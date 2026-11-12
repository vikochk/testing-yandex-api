from pydantic import BaseModel


class TestDataModel(BaseModel):
    __test__ = False

    login: str
    password: str
    oauth: str