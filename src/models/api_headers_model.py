from pydantic import BaseModel, Field, ConfigDict
from src.models.api_enums import ContentType


class RequestHeaders(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    authorization: str | None = Field(default=None, alias="Authorization")
    accept: ContentType | None = Field(default=None, alias="Accept")
    content_type: ContentType | None = Field(default=None, alias="Content-Type")