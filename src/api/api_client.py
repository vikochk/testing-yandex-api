import requests
from typing import Any


class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get_request(self, endpoint, headers: dict[str, str] | None = None, params: dict[str, Any] | None = None):
        url = f'{self.base_url}{endpoint}'
        response = requests.get(url, headers=headers, params=params)
        return response
    
    def post_request(self, endpoint, new_data_json: dict[str, Any] | None, 
                     headers: dict[str, str] | None = None, params: dict[str, Any] | None = None):
        url = f'{self.base_url}{endpoint}'
        response = requests.post(url, json=new_data_json, headers=headers, params=params)
        return response
    
    def put_request(self, endpoint, json_data: dict[str, Any] | None, 
                    headers: dict[str, str] | None = None, params: dict[str, Any] | None = None):
        url = f'{self.base_url}{endpoint}'
        return requests.put(url, json=json_data, headers=headers, params=params)

    def delete_request(self, endpoint: str, headers: dict[str, str] | None = None, params: dict[str, Any] | None = None):
        url = f'{self.base_url}{endpoint}'
        return requests.delete(url, headers=headers, params=params)