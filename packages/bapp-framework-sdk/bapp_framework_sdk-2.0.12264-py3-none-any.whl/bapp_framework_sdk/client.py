from typing import Literal

import requests


class BappFrameworkApiClient:
    base_url: str = 'https://api.bapp.ro/auto-api/'
    headers: dict = {}

    def __init__(self, base_url: str = None, token: str = None, bearer: str = None, app: str = 'erp'):
        self.headers = {
            'X-App-Slug': app,
        }
        if base_url:
            self.base_url = base_url
        if token:
            self.headers["Authorization"] = f"Token {token}"
        elif bearer:
            self.headers["Authorization"] = f"Bearer {bearer}"

        self.session = requests.Session()

    def api_call(self, method: Literal['get', 'post', 'put', 'patch', 'delete'], path: str, params: dict = None, json: dict = None, files: dict = None, data: dict = None):
        url = self.base_url + path
        response = self.session.request(method, url, headers=self.headers, params=params, files=files, data=data, json=json)
        return response

    def prepare_multipart(self, files):
        """Helper method to prepare data for multipart form submission"""
        # nu mai trebuie encodata si data daca are fisiere, se descurca requests sa trimita corect
        multipart_data = {}

        # Add files to the multipart data if they exist
        if files:
            multipart_data.update({key: (filename, open(filepath, 'rb')) for key, (filename, filepath) in files.items()})

        return multipart_data

    def handle_response(self, response):
        """Ensures the response is always parsed as JSON"""
        if response.status_code in [200, 201]:
            try:
                return response.json()
            except ValueError as e:
                raise ValueError(f"Invalid JSON response: {response.text}") from e
        # empty response after delete
        elif response.status_code == 204:
            return {}
        else:
            response.raise_for_status()

    def get_available_tasks(self):
        return self.handle_response(self.api_call('get', 'tasks'))

    def get_task_options(self, task_code: str):
        return self.handle_response(self.api_call('get', f'tasks', params={'code': task_code}))

    def call_task(self, task_code: str, data: dict = None, files: dict = None):
        if data is None:
            data = {}
        # Prepare multipart form data
        data.update({'code': task_code})
        if files:
            return self.handle_response(self.api_call('post', 'tasks', data=data, files=self.prepare_multipart(files)))
        # Call the API
        return self.handle_response(self.api_call('post', 'tasks', json=data))

    def introspect_content_type(self, content_type: str):
        return self.handle_response(self.api_call('get', f'introspect/{content_type}/'))

    def get_available_actions(self):
        return self.handle_response(self.api_call('get', 'actions'))

    def get_action_options(self, action_code):
        return self.handle_response(self.api_call('get', f'actions', params={'code': action_code}))

    def call_action(self, action_code: str, data: dict = None):
        json_data = {
            'code': action_code,
        }
        if data:
            json_data['payload'] = data
        return self.handle_response(self.api_call('post', 'actions', json=json_data))

    def get_available_widgets(self):
        return self.handle_response(self.api_call('get', 'widgets'))

    def get_widget_options(self, widget_code):
        return self.handle_response(self.api_call('get', f'widgets', params={'code': widget_code}))

    def call_widget(self, widget_code: str, data: dict = None):
        return self.handle_response(self.api_call('post', 'widgets', json={'code': widget_code, 'payload': data}))

    def list(self, content_type:str, params: dict = None):
        return self.handle_response(self.api_call('get', f'content-type/{content_type}/', params=params))

    def retrieve(self, content_type:str, pk: str, params: dict = None):
        return self.handle_response(self.api_call('get', f'content-type/{content_type}/{pk}/', params=params))

    def create(self, content_type:str, data: dict, files: dict = None):
        if files:
            return self.handle_response( self.api_call('post', f'content-type/{content_type}/', data=data, files=self.prepare_multipart(files)))
        return self.handle_response(self.api_call('post', f'content-type/{content_type}/', json=data))

    def update(self, content_type:str, pk: str, data: dict, files: dict = None):
        if files:
            return self.handle_response(self.api_call('post', f'content-type/{content_type}/', data=data, files=self.prepare_multipart(files)))
        return self.handle_response(self.api_call('put', f'content-type/{content_type}/{pk}/', json=data))

    def patch(self, content_type:str, pk: str, data: dict, files: dict = None):
        if files:
            return self.handle_response(self.api_call('post', f'content-type/{content_type}/', data=data, files=self.prepare_multipart(files)))
        return self.handle_response(self.api_call('patch', f'content-type/{content_type}/{pk}/', json=data))

    def delete(self, content_type:str, pk: str):
        return self.handle_response(self.api_call('delete', f'content-type/{content_type}/{pk}/'))
