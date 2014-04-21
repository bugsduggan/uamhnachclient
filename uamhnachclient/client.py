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

        if resp.status_code != 201:
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

    def groups(self):
        headers = self.headers
        headers['X-Auth-Token'] = self.get_token()

        resp = requests.get('%s/groups' % self.api_host,
                            headers=headers)

        if resp.status_code == 401:
            raise NotAuthorizedException
        if resp.status_code != 200:
            raise ClientException(resp.reason)

        data = resp.json()
        return data

    def create_group(self, group_name):
        payload = {
            'name': group_name,
        }

        headers = self.headers
        headers['X-Auth-Token'] = self.get_token()

        resp = requests.post('%s/groups' % self.api_host,
                             headers=headers,
                             data=json.dumps(payload))

        if resp.status_code == 401:
            raise NotAuthorizedException
        if resp.status_code != 201:
            raise ClientException

        data = resp.json()
        return data

    def group(self, group_id):
        headers = self.headers
        headers['X-Auth-Token'] = self.get_token()

        resp = requests.get('%s/group/%d' % (self.api_host, group_id),
                            headers=headers)

        if resp.status_code == 401:
            raise NotAuthorizedException
        if resp.status_code != 200:
            raise ClientException(resp.reason)

        data = resp.json()
        return data

    def add_to_group(self, group_id, user_id):
        payload = {
            user_id: 'add',
        }

        headers = self.headers
        headers['X-Auth-Token'] = self.get_token()

        resp = requests.put('%s/group/%d' % (self.api_host, group_id),
                            headers=headers,
                            data=json.dumps(payload))

        if resp.status_code == 401:
            raise NotAuthorizedException
        if resp.status_code != 200:
            raise ClientException(resp.reason)

        data = resp.json()
        return data

    def delete_from_group(self, group_id, user_id):
        payload = {
            user_id: 'delete',
        }

        headers = self.headers
        headers['X-Auth-Token'] = self.get_token()

        resp = requests.put('%s/group/%d' % (self.api_host, group_id),
                            headers=headers,
                            data=json.dumps(payload))

        if resp.status_code == 401:
            raise NotAuthorizedException
        if resp.status_code != 200:
            raise ClientException

        data = resp.json()
        return data

    def delete_group(self, group_id):
        headers = self.headers
        headers['X-Auth-Token'] = self.get_token()

        resp = requests.delete('%s/group/%d' % (self.api_host, group_id),
                               headers=headers)

        if resp.status_code == 401:
            raise NotAuthorizedException
        if resp.status_code != 200:
            raise ClientException

    def permissions(self):
        headers = self.headers
        headers['X-Auth-Token'] = self.get_token()

        resp = requests.get('%s/permissions' % self.api_host,
                            headers=headers)

        if resp.status_code == 401:
            raise NotAuthorizedException
        if resp.status_code != 200:
            raise ClientException(resp.reason)

        data = resp.json()
        return data

    def create_permission(self, permission_name):
        payload = {
            'name': permission_name,
        }

        headers = self.headers
        headers['X-Auth-Token'] = self.get_token()

        resp = requests.post('%s/permissions' % self.api_host,
                             headers=headers,
                             data=json.dumps(payload))

        if resp.status_code == 401:
            raise NotAuthorizedException
        if resp.status_code != 201:
            raise ClientException(resp.reason)

        data = resp.json()
        return data

    def permission(self, permission_id):
        headers = self.headers
        headers['X-Auth-Token'] = self.get_token()

        resp = requests.get('%s/permission/%d' % (self.api_host,
                                                  permission_id),
                            headers=headers)

        if resp.status_code == 401:
            raise NotAuthorizedException
        if resp.status_code != 200:
            raise ClientException(resp.reason)

        data = resp.json()
        return data

    def allow_group(self, permission_id, group_id):
        payload = {
            group_id: 'add',
        }

        headers = self.headers
        headers['X-Auth-Token'] = self.get_token()

        resp = requests.put('%s/permission/%d' % (self.api_host,
                                                  permission_id),
                            headers=headers,
                            data=json.dumps(payload))

        if resp.status_code == 401:
            raise NotAuthorizedException
        if resp.status_code != 200:
            raise ClientException(resp.reason)

        data = resp.json()
        return data

    def disallow_group(self, permission_id, group_id):
        payload = {
            group_id: 'delete',
        }

        headers = self.headers
        headers['X-Auth-Token'] = self.get_token()

        resp = requests.put('%s/permission/%d' % (self.api_host,
                                                  permission_id),
                            headers=headers,
                            data=json.dumps(payload))

        if resp.status_code == 401:
            raise NotAuthorizedException
        if resp.status_code != 200:
            raise ClientException(resp.reason)

        data = resp.json()
        return data

    def delete_permission(self, permission_id):
        headers = self.headers
        headers['X-Auth-Token'] = self.get_token()

        resp = requests.delete('%s/permission/%d' % (self.api_host,
                                                     permission_id),
                               headers=headers)

        if resp.status_code == 401:
            raise NotAuthorizedException
        if resp.status_code != 200:
            raise ClientException(resp.reason)
