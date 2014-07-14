import datetime
import json

import requests

from ..exceptions import BadRequestException, UnauthorizedException, NotFoundException, InternalServerErrorException, ForbiddenException
from ..utils import datetime_to_iso_format


class BaseAPI(object):
    http_exception_map = {
        400: BadRequestException,
        401: UnauthorizedException,
        403: ForbiddenException,
        404: NotFoundException,
        500: InternalServerErrorException,
    }

    def __init__(self, api_config, cache_finds):
        self.api_config = api_config
        self.cache_finds = cache_finds

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
            if 'close_to_location' in params:
                coords = map(str, params['close_to_location'])
                params['close_to_location'] = ','.join(coords)
            kwargs['params'] = params
            for param_key, param_val in params.items():
                if isinstance(param_val, datetime.datetime):
                    kwargs['params'][param_key] = datetime_to_iso_format(param_val)

        resp = getattr(requests, method)(full_path, **kwargs)

        if resp.status_code in self.http_exception_map:
            bad_request_json = resp.json()
            if resp.status_code == 400 and '_diagnostics' in bad_request_json and 'validation_failures' in bad_request_json['_diagnostics'] and len(bad_request_json['_diagnostics']['validation_failures']):
                printable_errors = []
                validation_failures = bad_request_json['_diagnostics']['validation_failures']
                for validation_dict_or_list in validation_failures:
                    if isinstance(validation_dict_or_list, dict):
                        for validation_dict_key, validation_dict_list in validation_dict_or_list.items():
                            for validation_error in validation_dict_list:
                                printable_errors.append('{0} {1}'.format(validation_dict_key, validation_error))
                    elif isinstance(validation_dict_or_list, list):
                        for validation_error in validation_dict_or_list:
                            printable_errors.append('{0}.'.format(validation_error))
                raise self.http_exception_map[resp.status_code](' '.join(printable_errors))
            else:
                raise self.http_exception_map[resp.status_code]

        if method != 'delete':
            return resp.json()
