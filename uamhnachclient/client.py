import json

import requests

from uamhnachclient.exc import *


class Client:

    def __init__(self, api_host=None, email=None, password=None):
        self.email = email
        self.password = password

        self.api_host = api_host
        if self.api_host.endswith('/'):
            self.api_host = self.api_host.rstrip('/')
        self.api_host = self.api_host + '/v1'

    @property
    def headers(self):
        return {
            'Content-Type': 'application/json',
        }

    def get_token(self):
        payload = {
            'email': self.email,
            'password': self.password,
        }

        resp = requests.post('%s/tokens' % self.api_host,
                             headers=self.headers,
                             data=json.dumps(payload))

        if resp.status_code == 200:
            raise ClientException(resp.reason)

        data = resp.json()
        return data['id']

    def users(self):
        headers = self.headers
        headers['X-Auth-Token'] = self.get_token()

        resp = requests.get('%s/users' % self.api_host,
                            headers=headers)

        if resp.status_code == 401:
            raise NotAuthorizedException
        if resp.status_code != 200:
            raise ClientException(resp.reason)

        data = resp.json()
        return data

    def create_user(self, name, email, password):
        payload = {
            'name': name,
            'email': email,
            'password': password,
        }

        headers = self.headers
        headers['X-Auth-Token'] = self.get_token()

        resp = requests.post('%s/users' % self.api_host,
                             headers=headers,
                             data=json.dumps(payload))

        if resp.status_code == 401:
            raise NotAuthorizedException
        if resp.status_code != 201:
            raise ClientException(resp.reason)

        data = resp.json()
        return data

    def user(self, user_id):
        headers = self.headers
        headers['X-Auth-Token'] = self.get_token()

        resp = requests.get('%s/user/%d' % (self.api_host, user_id),
                            headers=headers)

        if resp.status_code == 401:
            raise NotAuthorizedException
        if resp.status_code != 200:
            raise ClientException(resp.reason)

        data = resp.json()
        return data

    def update_user(self, user_id, name=None, email=None, password=None):
        payload = {}
        if name:
            payload['name'] = name
        if email:
            payload['email'] = email
        if password:
            payload['password'] = password

        headers = self.headers
        headers['X-Auth-Token'] = self.get_token()

        resp = requests.put('%s/user/%d' % (self.api_host, user_id),
                            headers=headers,
                            data=json.dumps(payload))

        if resp.status_code == 401:
            raise NotAuthorizedException
        if resp.status_code != 200:
            raise ClientException(resp.reason)

        data = resp.json()
        return data

    def delete_user(self, user_id):
        headers = self.headers
        headers['X-Auth-Token'] = self.get_token()

        resp = requests.delete('%s/user/%d' % (self.api_host, user_id),
                               headers=headers)

        if resp.status_code == 401:
            raise NotAuthorizedException
        if resp.status_code != 200:
            raise ClientException(resp.reason)
