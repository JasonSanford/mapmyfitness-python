import json

import requests

from .exceptions import BadRequestException, UnauthorizedException, NotFoundException, InternalServerErrorException, InvalidObjectException, InvalidSearchArgumentsException
from .inflators import RouteInflator
from .validators import RouteValidator


class APIConfig(object):
    uri_root = 'https://oauth2-api.mapmyapi.com'

    def __init__(self, api_key, access_token):

        self.api_key = api_key
        self.access_token = access_token
        self.api_root = '{0}/v7.0'.format(self.uri_root)


class BaseAPI(object):
    http_exception_map = {
        400: BadRequestException,
        403: UnauthorizedException,
        404: NotFoundException,
        500: InternalServerErrorException,
    }

    def __init__(self, api_config):
        self.api_config = api_config

    def all(self, **kwargs):
        if hasattr(self, 'validator_class'):
            self.validator = self.validator_class(search_kwargs=kwargs)
            if not self.validator.valid:
                raise InvalidSearchArgumentsException(self.validator)
        api_resp = self.call('get', self.path, params=kwargs)
        return api_resp

    def create(self, obj):
        if hasattr(self, 'validator_class'):
            self.validator = self.validator_class(create_obj=obj)
            if not self.validator.valid:
                raise InvalidObjectException(self.validator)

        if hasattr(self, 'inflator_class'):
            self.inflator = self.inflator_class(obj)
            data = self.inflator.inflated
        else:
            data = obj

        params = None
        if self.__class__.__name__ == 'Route':
            # Routes are special, and need to be created with additional params
            params = {'field_set': 'detailed'}

        api_resp = self.call('post', '{0}/'.format(self.path), data=data, extra_headers={'Content-Type': 'application/json'}, params=params)
        return api_resp


    def delete(self, id):
        self.call('delete', '{0}/{1}'.format(self.path, id))

    def find(self, id, **kwargs):
        api_resp = self.call('get', '{0}/{1}'.format(self.path, id), params=kwargs)
        return api_resp

    def call(self, method, path, data=None, extra_headers=None, params=None):
        full_path = self.api_config.api_root + path
        headers = {
            'Api-Key': self.api_config.api_key,
            'Authorization': 'Bearer {0}'.format(self.api_config.access_token)
        }
        if extra_headers is not None:
            headers.update(extra_headers)
        
        kwargs = {'headers': headers}

        if data is not None:
            kwargs['data'] = json.dumps(data)

        if params is not None:
            kwargs['params'] = params

        resp = getattr(requests, method)(full_path, **kwargs)

        if resp.status_code in self.http_exception_map:
            bad_request_json = resp.json()
            if resp.status_code == 400 and '_diagnostics' in bad_request_json and 'validation_failures' in bad_request_json['_diagnostics'] and len(bad_request_json['_diagnostics']['validation_failures']):
                printable_errors = []
                for validation_failure_list in bad_request_json['_diagnostics']['validation_failures']:
                    for validation_failure in validation_failure_list:
                        printable_errors.append('{0}.'.format(validation_failure))
                raise self.http_exception_map[resp.status_code](' '.join(printable_errors))
            else:
                raise self.http_exception_map[resp.status_code]

        if method != 'delete':
            return resp.json()

    def update(self, id, obj):
        if hasattr(self, 'validator_class'):
            self.validator = self.validator_class(obj)
            if not self.validator.valid:
                raise InvalidObjectException(self.validator)
        api_resp = self.call('put', '{0}/{1}'.format(self.path, id), data=obj, extra_headers={'Content-Type': 'application/json'})
        return api_resp


class Route(BaseAPI):
    path = '/route'
    validator_class = RouteValidator
    inflator_class = RouteInflator
