import requests
from urllib.parse import urljoin


class YANDEXAPIClient:
    API_BASE_URL = 'https://cloud-api.yandex.net/v1/disk/'

    def __init__(self, token):
        self.token = token

    def create_folder(self, folder_name):
        url_resources = 'resources?'
        params = {
            'path': folder_name
        }
        headers = {
            'Authorization': f'OAuth {self.token}'
        }
        response = requests.put(urljoin(self.API_BASE_URL, url_resources), params=params, headers=headers)
        return response

    def get_yandex_upload_photos(self, folder_name, image_name):
        url_resources = 'resources/upload/'
        params = {
            'path': f"{urljoin(folder_name, image_name)}"
        }
        headers = {
            'Authorization': f'OAuth {self.token}'
        }
        response = requests.get(urljoin(self.API_BASE_URL, url_resources), params=params, headers=headers)
        return response

    def get_file_info(self, folder_name, image_name):
        url_resources = 'resources?'
        params = {
            'path': f"{urljoin(folder_name, image_name)}"
        }
        headers = {
            'Authorization': f'OAuth {self.token}'
        }
        response = requests.get(urljoin(self.API_BASE_URL, url_resources), params=params, headers=headers)
        return response
