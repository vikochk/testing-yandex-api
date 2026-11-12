from typing import Optional
from pydantic import BaseModel


class TrashResourceModel(BaseModel):
    name: str
    path: str
    origin_path: Optional[str] = None
    type: str
    mime_type: Optional[str] = None
    size: Optional[int] = None
    md5: Optional[str] = None