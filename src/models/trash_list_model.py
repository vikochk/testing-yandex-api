from typing import List
from pydantic import BaseModel, Field
from src.models.trash_resource_model import TrashResourceModel


class EmbeddedTrashItems(BaseModel):
    items: List[TrashResourceModel]


class TrashListModel(BaseModel):
    embedded: EmbeddedTrashItems | None = Field(default=None, alias="_embedded")