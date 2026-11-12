import requests
from http import HTTPStatus
from typing_extensions import Unpack

from src.api.response import Response
from src.api.api_client import APIClient

from src.models.link_model import LinkModel
from src.models.trash_list_model import TrashListModel
from src.models.yandex_error_model import YandexErrorModel
from src.models.trash_resource_model import TrashResourceModel

from src.models.api_headers_model import RequestHeaders
from src.models.api_enums import RootLocation, ContentType
from src.models.api_params_models import GetUploadLinkParams, TrashResourceParams, DeleteResourceParams, TrashListParams, MoveResourceParams


class YandexApiClient(APIClient):
    BASE_URL = 'https://cloud-api.yandex.net/v1/disk'

    ENDPOINT_RESOURCES = '/resources'
    ENDPOINT_UPLOAD = '/resources/upload'
    ENDPOINT_MOVE = '/resources/move'
    ENDPOINT_TRASH = '/trash/resources'
    ENDPOINT_RESTORE = '/trash/resources/restore'

    def __init__(self, oauth_token):
        super().__init__(self.BASE_URL)
        headers_model = RequestHeaders(
            Authorization=f'OAuth {oauth_token}',
            Accept=ContentType.JSON
        )
        
        self.headers = headers_model.model_dump(by_alias=True, exclude_none=True)

    def _get_upload_link(self, **kwargs: Unpack[GetUploadLinkParams]) -> Response[LinkModel|YandexErrorModel]:
        raw_response = self.get_request(self.ENDPOINT_UPLOAD, headers=self.headers, params=kwargs)
        return Response(raw_response, model_type=LinkModel|YandexErrorModel)

    def _upload_file_to_link(self, upload_url, content) -> Response[None]:
        data = content.encode('utf-8') if isinstance(content, str) else content
        raw_response = requests.put(upload_url, data=data)
        return Response(raw_response, model_type=None)

    def upload_file(self, file_content: str | bytes, destination: str, 
                    location: RootLocation = RootLocation.DISK, overwrite: bool = False) -> Response[None|YandexErrorModel]:
        upload_params: GetUploadLinkParams = {
            'path': location + destination,
            'overwrite': str(overwrite).lower()
        }

        link_response = self._get_upload_link(**upload_params)
        if link_response.status_code != HTTPStatus.OK:
            return Response(link_response.raw, model_type=YandexErrorModel)
        
        if isinstance(link_response.data, LinkModel):
            upload_url = link_response.data.href
            return self._upload_file_to_link(upload_url, file_content)
        
        return Response(link_response.raw, model_type=YandexErrorModel)

    def move_or_rename_resource(self, from_name, to_name, from_location: RootLocation = RootLocation.DISK, 
                                to_location: RootLocation = RootLocation.DISK) -> Response[LinkModel|YandexErrorModel]:
        move_params: MoveResourceParams = {
            'from': from_location + from_name,
            'path': to_location + to_name
        }
        raw_response = self.post_request(self.ENDPOINT_MOVE, new_data_json=None, headers=self.headers, params=move_params)
        return Response(raw_response, model_type=LinkModel|YandexErrorModel)

    def get_trash_resource(self, filename: str, location: RootLocation = RootLocation.TRASH) -> Response[TrashResourceModel|YandexErrorModel]:
        full_path = filename if filename.startswith(RootLocation.TRASH) else location + filename
        trash_params: TrashResourceParams = {
            'path': full_path
        }
        raw_response = self.get_request(self.ENDPOINT_TRASH, headers=self.headers, params=trash_params)
        return Response(raw_response, model_type=TrashResourceModel|YandexErrorModel)

    def restore_trash_resource(self, filename: str, location: RootLocation = RootLocation.TRASH) -> Response[LinkModel|YandexErrorModel]:
        full_path = filename if filename.startswith(RootLocation.TRASH) else location + filename
        trash_params: TrashResourceParams = {
            'path': full_path
        }
        raw_response = self.put_request(self.ENDPOINT_RESTORE, json_data=None, headers=self.headers, params=trash_params)
        return Response(raw_response, model_type=LinkModel|YandexErrorModel)

    def delete_resource(self, filename: str, location: RootLocation = RootLocation.DISK, permanently: bool = True) -> Response[YandexErrorModel]:
        delete_params: DeleteResourceParams = {
            'path': location + filename,
            'permanently': str(permanently).lower()
        }
        raw_response = self.delete_request(self.ENDPOINT_RESOURCES, headers=self.headers, params=delete_params)
        return Response(raw_response, model_type=YandexErrorModel)
    
    def get_trash_list(self, limit: int = 20) -> Response[TrashListModel|YandexErrorModel]:
        trash_list_params: TrashListParams = {
            'limit': limit
        }
        raw_response = self.get_request(self.ENDPOINT_TRASH, headers=self.headers, params=trash_list_params)
        return Response(raw_response, model_type=TrashListModel|YandexErrorModel)