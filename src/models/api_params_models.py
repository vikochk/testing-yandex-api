from typing import TypedDict


class GetUploadLinkParams(TypedDict):
    path: str
    overwrite: str


class TrashResourceParams(TypedDict):
    path: str


class DeleteResourceParams(TypedDict):
    path: str
    permanently: str


class TrashListParams(TypedDict):
    limit: int


MoveResourceParams = TypedDict('MoveResourceParams', {
    'from': str,
    'path': str
})