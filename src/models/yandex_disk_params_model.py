from http import HTTPStatus
from pydantic import BaseModel


class InitialFileParams(BaseModel):
    name: str
    expected_upload_status: int


class RenamedFileParams(BaseModel):
    name_ending: str
    expected_type_in_trash: str 
    expected_rename_status: HTTPStatus = HTTPStatus.CREATED
    expected_overwrite_status: HTTPStatus = HTTPStatus.CREATED
    expected_restore_status: HTTPStatus = HTTPStatus.CREATED
    expected_delete_status: HTTPStatus = HTTPStatus.NO_CONTENT


class YandexDiskParamsModel(BaseModel):
    initial_file: InitialFileParams
    renamed_file: RenamedFileParams