from pydantic import BaseModel


class LinkModel(BaseModel):
    href: str
    method: str
    templated: bool